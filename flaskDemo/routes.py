import os
import secrets
import re
import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, current_app
from flaskDemo import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import StringField
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, Permission, RoleNeed
from flaskDemo.models import User, UserInfo, Order, Status, OrderDetail, Product, Category, Payment
from flaskDemo.forms import LoginForm, RegistrationForm, AddNewUserForm, CheckoutForm, ProductForm, ProductUpdateForm, CategoryForm, CategoryUpdateForm, UserInfoForm, UpdateUserInfoForm, SearchForm
from datetime import datetime, timedelta
from sqlalchemy import or_, update, and_
import mysql.connector
from mysql.connector import Error
import yaml

admin_permission = Permission(RoleNeed('admin'))

# Configure db
database = yaml.load(open('./flaskDemo/database.yaml'))

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    products = Product.query.all()
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('home.html', title='Products', products=products,form1 = search)

@app.route("/about", methods=['GET', 'POST'])
def about():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('home.html', content='About',form1 = search)

@app.route("/logout")
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('home', content='Log out'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.passwords, form.password.data):
            login_user(user, remember=form.remember.data)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.userID))

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
             
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, passwords=hashed_password, roleID=1, timeStamp=datetime.now())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    search = SearchForm(request.form)
    return render_template('register.html', title='Register', form=form,form1 = search)

@app.route("/cart", methods=['GET', 'POST'])
@login_required
def cart():
    # statusID - 1: pending, 2: checkout, 3: canceled
    form = CheckoutForm()
    order = Order.query.filter(and_(Order.userID == current_user.userID, Order.statusID == 1)).first()
    if order == None:
        order = Order(userID=current_user.userID, statusID=1, date_updated=datetime.now(), totalPrice = 0)
        db.session.add(order)
        db.session.commit()
    
    orderDetail = OrderDetail.query.filter(OrderDetail.orderID == order.orderID).all()
    products = []
    if len(orderDetail) > 0:
        products = productByCartDetail(orderDetail)

    total = 0
    for product in products:
        total += (product.price * product.order_quantity)
    #check out
    if form.validate_on_submit():
        products_mapping = []
        for product in products:
            total += (product.price * product.order_quantity)
            if product.quantity >= product.order_quantity:
                products_mapping.append({
                    'productID': product.productID,
                    'quantity': product.quantity - product.order_quantity
                })
            else:
                flash(product.productName + ' has only ' + str(product.quantity) + ' left', 'danger')
                return render_template('cart.html', products = products, form = form, total = total)
        
        db.session.bulk_update_mappings(Product, products_mapping)
        db.session.commit()
        return redirect(url_for('shipping_address'))
    return render_template('cart.html', products = products, form = form, total = total)

@app.route("/add/<productID>", methods=['GET', 'POST'])
@login_required
def add_cart(productID):
    # statusID - 1: pending, 2: checkout, 3: canceled
    product = Product.query.get_or_404(productID)
    order = Order.query.filter(Order.userID == current_user.userID, Order.statusID == 1).first()
    if order == None:
        order = Order(userID=current_user.userID, statusID=1, date_updated=datetime.now(), totalPrice = 0)
        db.session.add(order)
        db.session.commit()

    orderDetail = OrderDetail.query.filter(OrderDetail.orderID == order.orderID, OrderDetail.productID == productID).first()
    if orderDetail == None:
        orderDetail = OrderDetail(orderID=order.orderID, productID=productID, quantity = 1)
        db.session.add(orderDetail)
    else:
        orderDetail.quantity += 1
    db.session.commit()
    flash('You now ordered ' + str(orderDetail.quantity) + ' ' + product.productName, 'success')
    return redirect(url_for('home'))

@app.route("/remove/<orderID>/<productID>", methods=['GET', 'POST'])
@login_required
def cart_delete(orderID,productID):
    orderDetail = OrderDetail.query.filter(OrderDetail.orderID == orderID, OrderDetail.productID == productID).first()
    if orderDetail == None:
        return redirect(url_for('cart'))
    db.session.delete(orderDetail)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route("/shipping", methods=['GET', 'POST'])
@login_required
def shipping_address():
    user_infos = UserInfo.query.filter(UserInfo.userID == current_user.userID).all()
    return render_template('shipping_address.html', infos = user_infos)

@app.route("/payment/<shipping_id>", methods=['GET', 'POST'])
@login_required
def payment(shipping_id):
    user_infos = UserInfo.query.filter(UserInfo.infoID == shipping_id).first()
    form = CheckoutForm()
    subquery = db.session.query(User.userID).filter(User.userID==current_user.userID).subquery()
    order = Order.query.filter(and_(Order.statusID == 1, Order.userID == subquery)).first()

    ''' Connect to MySQL database '''
    try:
        conn = mysql.connector.connect(host=database['mysql_host'],
                                       port=database['mysql_port'],
                                      database=database['mysql_db'],
                                      user=database['mysql_user'],
                                      password=database['mysql_password'])
        if conn.is_connected():
            cursor = conn.cursor()
        else:
            return('problem')

        sqlRaw = "SELECT product.productID, product.productName, product.description, product.categoryID, product.price, "
        sqlRaw += "product.quantity, orders_detail.quantity, orders_detail.orderID, SUM(product.price * orders_detail.quantity) "
        sqlRaw += "FROM orders_detail, product "
        sqlRaw += "WHERE orders_detail.orderID = {0} AND orders_detail.productID = product.productID "
        sqlRaw += "GROUP BY product.productID, orders_detail.quantity"
        cursor.execute(sqlRaw.format(order.orderID))
        
        products = cursor.fetchall()
        print(products)
    except Error as e:
        print(e)
        return redirect(url_for("home"))
 
    finally:
        conn.close()

    total = 0
    for product in products:
        total += product[8]
    #check out
    if form.validate_on_submit():
        products_mapping = []
        for product in products:
            total += product[8]
            products_mapping.append({
                    'productID': product[0],
                    'quantity': product[5] - product[6]
                })
        order.totalPrice = total
        order.statusID = 2
        payment = Payment(orderID = order.orderID, userID = current_user.userID, date = datetime.now(), totalPrice = total, shippingMethod = "Not yet")
        db.session.add(payment)
        db.session.bulk_update_mappings(Product, products_mapping)
        db.session.commit()
        flash('Check out success', 'success')
        return redirect(url_for('home'))
    return render_template('payment.html', form = form, info = user_infos, products = products, total = total)


@app.route('/users')
@admin_permission.require(http_exception=403)
def users():
    users = User.query.filter(User.roleID == 1).all()
    return render_template('users.html', content='Users Administrators', users = users)

@app.route("/users/<userID>", methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def users_detail(userID):
    user = User.query.get_or_404(userID)
    user_infos = UserInfo.query.filter(UserInfo.userID == userID).all()
    return render_template('user.html', content='Users Detail Administrators', user = user, infos = user_infos)

@app.route("/users/<userID>/delete", methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def delete_user(userID):
    user = User.query.get_or_404(userID)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users'))

@app.route('/users/add', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def add_user():
    form = AddNewUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role = 1
        if form.isAdmin.data == 1:
            role = 2
        user = User(username=form.username.data, passwords=hashed_password, roleID=role, timeStamp=datetime.now())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('add_user.html', title='Add new user', form=form)

@app.route('/order', defaults={'type_orders': 'expired'})
@app.route('/order/<type_orders>')
@admin_permission.require(http_exception=403)
def orders(type_orders):
    status_type = 1

    if type_orders == 'pending':
        status_type = 1
    elif type_orders == 'checkout':
        status_type = 2

    one_days_ago = datetime.utcnow() - timedelta(days=1)
    orders = []
    
    if type_orders == 'expired':
        orders = Order.query.join(User, Order.userID == User.userID)\
                                .add_columns(User.username, Order.date_updated, Order.totalPrice, Order.orderID)\
                                .join(OrderDetail, Order.orderID == OrderDetail.orderID)\
                                .add_columns(OrderDetail.productID, OrderDetail.quantity)\
                                .join(Product, OrderDetail.productID == Product.productID)\
                                .add_columns(Product.productName, Product.price)\
                                .filter(Order.statusID == status_type, Order.date_updated < one_days_ago).all()
    else: 
        orders = Order.query.join(User, Order.userID == User.userID)\
                                .add_columns(User.username, Order.date_updated, Order.totalPrice, Order.orderID)\
                                .join(OrderDetail, Order.orderID == OrderDetail.orderID)\
                                .add_columns(OrderDetail.productID, OrderDetail.quantity)\
                                .join(Product, OrderDetail.productID == Product.productID)\
                                .add_columns(Product.productName, Product.price)\
                                .filter(Order.statusID == status_type).all()

    return render_template('order.html', orders = orders, type_orders = type_orders)

@app.route('/order/<orderID>/delete')
@admin_permission.require(http_exception=403)
def order_delete(orderID):
    order = Order.query.filter(Order.orderID == orderID).first()
    if order != None:
        db.session.delete(order)
        db.session.commit()
        flash("Delete order success", "success")
    return redirect(url_for('orders'))

@app.route('/order/<orderID>/cancel')
@admin_permission.require(http_exception=403)
def order_cancel(orderID):
    order = Order.query.filter(Order.orderID == orderID).first()
    if order != None:
        order.statusID = 3
        db.session.commit()
        flash("Cancel order success", "success")
    return redirect(url_for('orders'))

@app.errorhandler(403)
def page_not_found(e):
    return redirect(url_for('home'))

def productByCartDetail(orderDetail):
    filterQuery = []
    query = OrderDetail.query.join(Product,OrderDetail.productID == Product.productID)\
                            .add_columns(Product.productID, Product.productName, Product.description, Product.categoryID, Product.price, Product.quantity, Product.image, OrderDetail.quantity.label("order_quantity"), OrderDetail.orderID)
    for detail in orderDetail:
        filterQuery.append(OrderDetail.productID == detail.productID)
    return query.filter(and_(or_(*filterQuery), OrderDetail.orderID == orderDetail[0].orderID)).all()

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/product/new", methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def new_product():
    form = ProductForm()
    image_file = ''
    if form.validate_on_submit(): 
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            #print(picture_file)
            image_file = url_for('static', filename='profile_pics/' + picture_file)
        product = Product(description=form.description.data,image=image_file
            ,price=form.price.data,quantity=form.quantity.data, categoryID=form.categoryName.data, productName=form.productName.data)
        db.session.add(product)
        db.session.commit()
        flash('You have added a new product!', 'success')
        return redirect(url_for('product_home'))
    return render_template('create_product.html', title='New Product',image_file=image_file,
                           form=form, legend='New Product')


@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_home.html', title=product.productID, product=product)


@app.route("/product/product_home", methods=['GET'])
@admin_permission.require(http_exception=403)
def product_home(): 
    try:
        conn = mysql.connector.connect(host=database['mysql_host'],
                                       port=database['mysql_port'],
                                      database=database['mysql_db'],
                                      user=database['mysql_user'],
                                      password=database['mysql_password'])
        if conn.is_connected():
            cursor = conn.cursor()
        else:
            return('problem')
        sqlRaw = "SELECT product.productID, product.productName, product.description, product.categoryID, "
        sqlRaw += "product.image, product.price, product.quantity, category.categoryName "
        sqlRaw += "FROM product "
        sqlRaw += "LEFT JOIN category ON product.categoryID = category.categoryID "
        cursor.execute(sqlRaw)
        
        products = cursor.fetchall()
        print(products)
    except Error as e:
        print(e)
        return redirect(url_for("home"))
 
    finally:
        conn.close()

    return render_template('product_home.html', results=products)


@app.route("/product_home/<int:product_id>/update", methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def update_product(product_id):
    #product = Product.query.get_or_404(product_id)
    #category = Category.query.get_or_404(product.categoryID)

    product = Product.query.join(Category,Category.categoryID == Product.categoryID) \
               .add_columns(Product.productID, Product.categoryID, Product.description, Product.image, Product.price, Product.quantity, Category.categoryName).all()
    form = ProductUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image_file = url_for('static', filename='profile_pics/' + picture_file)
        #product.image = image_file
        product.productName = form.productName.data
        product.categoryName = form.categoryName.data
        product.price = form.price.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        db.session.configure()
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('product_home'))
    elif request.method == 'GET': 
        form.price.data = product.price
        form.description.data = product.description
        form.quantity.data = product.quantity
        form.categoryName.data = product.categoryName
        form.productName.data = product.productName
    image_file = url_for('static', filename='profile_pics/' + picture_file)
    return render_template('update_product.html', title='Update Product', image_file=image_file,
                           form=form, legend='Update Product')


@app.route("/product_home/<product_id>/delete", methods=['GET','POST'])
@admin_permission.require(http_exception=403)
def delete_prodcut(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('The Product has been deleted!', 'success')
    return redirect(url_for('product_home'))



@app.route("/category/new", methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def new_category():
    form = CategoryForm()
    # if form.validate_on_submit():
    #     category = Category(categoryName=form.categoryName.data)
    #     db.session.add(Category)
    #     db.session.commit()
    #     flash('Your post has been created!', 'success')
    #     return redirect(url_for('category_home'))
    return render_template('create_category.html', title='New category',
                           form=form, legend='New category')

@app.route("/category/<int:category_id>")
def category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', title=Category.categoryID, category=category)

@app.route("/category/category_home", methods=['GET'])
@login_required
def category_home(): 
    results2 = Category.query.all()
    return render_template('category_home.html', results2=results2)



@app.route("/userinfo_category/<category_id>/update", methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the nickname from the form
        category.categoryID=form.categoryID.data
        category.categoryName=form.categoryName.data 
        db.session.configure()
        db.session.commit()
        flash('Your info has been updated!', 'success')
        return redirect(url_for('category_home'))
    elif request.method == 'GET':             
        form.categoryID.data = category.categoryID   # notice that we ARE passing the nickname to the form
        form.categoryName.data =category.categoryName
       
    return render_template('update_category.html', title='Update category',
                           form=form, legend='Update category')          # note the update template!

@app.route("/category_home/<category_id>/delete", methods=['GET','POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('The userinfo has been deleted!', 'success')
    return redirect(url_for('category_home'))
@app.route("/account")
@login_required
def userinfo_home(): 
    userinfo = UserInfo.query.all()
    return render_template('userinfo_home.html', userinfo = userinfo)


@app.route("/userinfo/new", methods=['GET', 'POST'])
@login_required
def new_userinfo():
    form = UserInfoForm()
    if form.validate_on_submit():
        userinfo = UserInfo(nickname=form.nickname.data,userID = current_user.userID,fullname=form.fullname.data, address=form.address.data,zipcode=form.zipcode.data,city=form.city.data,state=form.state.data,phone=form.phone.data)
        db.session.add(userinfo)
        db.session.commit()
        flash('You have added a new info!', 'success')
        return redirect(url_for('userinfo_home'))
    return render_template('create_userinfo.html', title='New Info',
                           form=form, legend='New Info')

@app.route("/userinfo/<infoID>")
@login_required
def userinfo(infoID):
    userinfo = UserInfo.query.get_or_404(infoID)
    return render_template('userinfo.html', title=userinfo.infoID, userinfo=userinfo)

@app.route("/userinfo_home/<infoID>/update", methods=['GET', 'POST'])
@login_required
def update_userinfo(infoID):
    userinfo = UserInfo.query.get_or_404(infoID)
    form = UpdateUserInfoForm()
    if form.validate_on_submit():          # notice we are are not passing the nickname from the form
        userinfo.nickname=form.nickname.data
        userinfo.fullname=form.fullname.data 
        userinfo.address=form.address.data
        userinfo.zipcode=form.zipcode.data
        userinfo.city=form.city.data
        userinfo.state=form.state.data
        userinfo.phone=form.phone.data
        db.session.configure()
        db.session.commit()
        flash('Your info has been updated!', 'success')
        return redirect(url_for('userinfo_home'))
    elif request.method == 'GET':             
        form.nickname.data = userinfo.nickname   # notice that we ARE passing the nickname to the form
        form.fullname.data=userinfo.fullname
        form.address.data=userinfo.address
        form.zipcode.data=userinfo.zipcode
        form.city.data=userinfo.city
        form.state.data=userinfo.state
        form.phone.data=userinfo.phone
       
    return render_template('update_userinfo.html', title='Update Info',
                           form=form, legend='Update Info')          # note the update template!

@app.route("/userinfo_home/<infoID>/delete", methods=['GET','POST'])
@login_required
def delete_userinfo(infoID):
    userinfo = UserInfo.query.get_or_404(infoID)
    db.session.delete(userinfo)
    db.session.commit()
    flash('The userinfo has been deleted!', 'success')
    return redirect(url_for('userinfo_home'))

    
@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('home.html', form1=search) 


    
    


@app.route('/results')
def search_results(search):
    search = SearchForm(request.form)
    results = []
    search_string = search.data['search']
   
 
    if search_string:
        if search.data['select'] == 'Category':
            qry = Product.query.join(Category,Category.categoryID == Product.categoryID) \
               .add_columns(Category.categoryName, Product.productName, Product.price, Product.image, Product.price).filter(
                    Category.categoryName.contains(search_string))
            results = [item[0] for item in qry.all()]
        elif search.data['select'] == 'Price':
            qry = Product.query.join(Category,Category.categoryID == Product.categoryID) \
               .add_columns(Category.categoryName, Product.productName, Product.price, Product.image, Product.price).filter(
                    Product.price.contains(search_string))
            results = [item[0] for item in qry.all()]
        elif search.data['select'] == 'ProductName':
            qry = Product.query.join(Category,Category.categoryID == Product.categoryID) \
               .add_columns(Category.categoryName, Product.productName, Product.price, Product.image, Product.price).filter(
                    Product.productName.contains(search_string))
            results =  [item[0] for item in qry.all()]
        else:
            qry = Product.query.join(Category,Category.categoryID == Product.categoryID) \
               .add_columns(Category.categoryName, Product.productName, Product.price, Product.image, Product.price).all()
            results = qry
    else:
        qry = Product.query.join(Category,Category.categoryID == Product.categoryID) \
               .add_columns(Category.categoryName, Product.productName, Product.price, Product.image, Product.price).all()
        results = qry
 
    if not results:
        flash('No results found!')

    print(results)
   
        # display results
    return render_template('home.html', products=results,form1 = search )







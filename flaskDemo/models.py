from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model, UserMixin):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}
    roleID = db.Column(db.Integer, primary_key=True, nullable=False)
    roleName = db.Column(db.String(25), nullable=False)
    user = db.relationship("User",backref = 'role',lazy = True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    passwords = db.Column(db.String(70), nullable=False)
    roleID = db.Column(db.Integer, db.ForeignKey('role.roleID'), nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False)
    userinfo = db.relationship("UserInfo",backref = 'user',lazy = True)
    def get_id(self): 
        return (self.userID)

class UserInfo(db.Model, UserMixin):
    __tablename__ = 'user_info'
    __table_args__ = {'extend_existing': True}
    infoID = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.Integer, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    fullname = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text(30), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

class Category(db.Model, UserMixin):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}
    categoryID = db.Column(db.Integer, primary_key=True, nullable=False)
    categoryName = db.Column(db.String(25), nullable=False) 
    #product = db.relationship('Product',backref='Cateogy',lazy = True)
  

class Product(db.Model, UserMixin):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}
    productID = db.Column(db.Integer, primary_key=True, nullable=False)
    productName = db.Column(db.String(50), nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey('category.categoryID'), nullable=False)
    description = db.Column(db.String(300), unique=True, nullable=False)
    image = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Status(db.Model, UserMixin):
    __tablename__ = 'status'
    __table_args__ = {'extend_existing': True}
    statusID = db.Column(db.Integer, primary_key=True, nullable=False)
    statusName = db.Column(db.String(25), nullable=False)

class Order(db.Model, UserMixin):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    orderID = db.Column(db.Integer, primary_key=True, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    statusID = db.Column(db.Integer, db.ForeignKey('status.statusID'), nullable=False)
    totalPrice = db.Column(db.Integer, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=False)

class OrderDetail(db.Model, UserMixin):
    __tablename__ = 'orders_detail'
    __table_args__ = {'extend_existing': True}
    orderID = db.Column(db.Integer, db.ForeignKey('orders.orderID'), primary_key=True, nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey('product.productID'), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Payment(db.Model, UserMixin):
    __tablename__ = 'payment'
    __table_args__ = {'extend_existing': True}
    paymentID = db.Column(db.Integer, primary_key=True, nullable=False)
    orderID = db.Column(db.Integer, db.ForeignKey('orders.orderID'), primary_key=True, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), primary_key=True, nullable=False)
    date = db.Column('datetime', db.DateTime, nullable=False)
    totalPrice = db.Column(db.Integer, nullable=False)
    shippingMethod = db.Column(db.String(50), unique=True, nullable=False)



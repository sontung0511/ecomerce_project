from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Product, Category, UserInfo
from wtforms.fields import DateField
from flask_wtf import Form


category = Category.query.all()
regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
regex=regex1 + regex2
results=list()
myChoices = []
for row in category:
    myChoices.append((row.categoryID, row.categoryName))


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_password(self, password):
        if len(password.data) < 5:
            raise ValidationError('Password must be at least 5 characters.')

class AddNewUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    isAdmin = BooleanField()
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_password(self, password):
        if len(password.data) < 5:
            raise ValidationError('Password must be at least 5 characters.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class CheckoutForm(FlaskForm):
    quantity = StringField()
    submit = SubmitField('Update')

class ProductForm(FlaskForm):
    price = StringField('Price', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    quantity = StringField('quantity', validators = [DataRequired()])
    picture = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png'])])
    productName = StringField('Product Name', validators=[DataRequired()])
    categoryName = SelectField("Product categoryName",choices=myChoices, coerce=int)
    submit = SubmitField('ADD')


class ProductUpdateForm(FlaskForm):
    price = StringField('Price', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    quantity = StringField('quantity', validators = [DataRequired()])
    picture = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png'])])
    productName = StringField('Product Name', validators=[DataRequired()])
    categoryName = SelectField("Product categoryName",choices=myChoices, coerce=int)
    submit = SubmitField('Update')

class CategoryForm(FlaskForm):
    #categoryID = SelectField("Product categoryName", validators=[DataRequired()])
    categoryName = StringField("Product categoryName", validators=[DataRequired()])
    submit = SubmitField('Update')

class CategoryUpdateForm(FlaskForm):
    categoryName = SelectField("Product categoryName", validators=[DataRequired()])
    submit = SubmitField('Update')

#1
class UserInfoForm(FlaskForm):
    nickname = StringField('Give a Name to this User Info!',validators=[DataRequired()])
    fullname = StringField('Full Name',validators=[DataRequired(), Length(min=2, max=20)])
    address = TextAreaField('Address', validators=[DataRequired() ])
    zipcode = IntegerField('Zip Code',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField('State',validators=[DataRequired(), Length(min=2, max=10)])
    phone = IntegerField('Phone Number',validators=[DataRequired()])
    submit = SubmitField('Add Info')
    def validate_userinfo(self, nickname):
        user = UserInfo.query.filter_by(nickname=nickname.data).first()
        if user:
            raise ValidationError('This Nickname is taken. Please choose a different one.')
#   
#2
class UpdateUserInfoForm(FlaskForm):
    nickname = StringField('Give a Name to this User Info!',validators=[DataRequired()])
    fullname = StringField('Full Name',validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    zipcode = IntegerField('Zip Code',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField('State',validators=[DataRequired(), Length(min=2, max=10)])
    phone = IntegerField('Phone Number',validators=[DataRequired()])
    submit = SubmitField('Edit Info')
    
    def validate_userinfo(self, userinfoid):
        user = UserInfo.query.filter_by(userinfoid=userinfoid.data).first()
        if user:
            raise ValidationError('This Nickname is taken. Please choose a different one.')

class SearchForm(FlaskForm):
    choices = [('Category', 'Category'),
               ('Price', 'Price'),
               ('ProductName', 'ProductName')]
    select = SelectField('Search for:', choices=choices)
    search = StringField('')


              



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_principal import Principal, Permission, RoleNeed
from flask_principal import identity_loaded, RoleNeed, UserNeed


app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:8889/ecommerce1' #Luu
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/ecommerce_ddl' #Albert
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://liquidten:Magnum88@127.0.0.1:3307/ecommerce1' #Saleep


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# load the extension
principals = Principal(app)


from flaskDemo import routes
from flaskDemo import models

models.db.create_all()

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'userID'):
        identity.provides.add(UserNeed(current_user.userID))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roleID'):
        if current_user.roleID == 1:
            identity.provides.add(RoleNeed('user'))
        else:
            identity.provides.add(RoleNeed('admin'))

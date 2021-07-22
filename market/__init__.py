from flask import Flask
from flask_sqlalchemy import SQLAlchemy # database conversion library
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '59082d3e65e110369a9b3a3e'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page' # with @login_required, login_page will render first if not login yet
login_manager.login_message_category = 'info'

from market import routes

**In this note file, `market.py` is the main python file**

`app = Flask(__name__)` --> __name__ is magic variable. Variable that can be called from any python file.
`@app.route("/")` is Decorators for the route function (routing to a page)
`def home_page():    return render_template('home.html')` is routing function
    
`$ export FLASK_APP=<hello>.py`  # Set in the command. Then can run with:
`$ flask run`
- When running, Host ip an port will be available.
- `Debug mode: off`  --> by default (If OFF, the web cannot synchronize with the code changes)
`$ export FLASK_ENV=development` --> Debug mode: On (In production, the Debug mode should be off.)

Writing a long **HTML** in a `def` is not the good way. We should write in a separate file and call easily. Page template should place in `template` folder (package can understand there html files are located).
- *return render_template("<name.html>")*

Styling of the pages, [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction/) (4.5) framework wil be used.
- `<head>Name</head>` --> Name of the tab name
- `<body>Name</body>` --> Text in the web page

If we put two Decorator `@app.route()` above the route, it will create two routes for a **HTML** file.
```
from flask import render_template
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')
```

To send data from this route to html, we need to use a new web template engine called **Jinja Template**.
```
<!-- .py -->
@app.route('/market')
def market_page():
    return render_template('market.html', item_name='item')

<!-- .html -->
<p>{{ item_name }}</p>
```

Basic template will be needed for all route. We should not do copying the template and editing. We should use **Template Inheritance** which means keeping a base template and new will inherit from base. `base.html` is created and it can be extended from any **HTML** with the tab title:
```
<!-- at <inherit>.html -->
{% extends 'base.html' %}
{% block title %}
  Home Page
{% endblock %}
{% block content %}
    <!-- 
    can write any HTML between the content block
    -->
{% endblock %}
```
```
<!-- at <base>.html -->
<title>
    {% block title %}
    {% endblock %}
</title>
<body>
    {% block content %}
    {% endblock %}
</body>
```

To link a button or a tab with the route, `<a href="#">Button</a>` can be used. We can use two methods:
- `<a class="nav-link" href="/home">Market</a>`: using decorator route
- `<a class="nav-link" href="{{ url_for('home_page') }}">Market</a>`: using route function name


### Database Models
Will use [SQlite3](https://docs.python.org/3/library/sqlite3.html) which can be easily connected with `Flask`.
- `$ pip install flask-sqlalchemy`: can do conversion from python info to database info

Create a database class with SQLALCHEMY.
```
<!-- <python_filename>.py -->
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # database conversion library

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # limiting the length of string, cannot be blank, cannot be same name
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item{self.name}'
```
And run a python shell to create database with a list of items at the same location and to check **SQLAlchemy**:
```
>>> from <python_filename> import db
>>> db.create_all()

>>> from <python_filename> import Item      # item classname
>>> item1 = Item(name='IPhone 10', price=500, barcode='122123783942', description="Iphone 10 new")
>>> db.session.add(item1)
>>> db.session.commit()
>>> Item.query.all()                        # query all item

```
After creating a database with a list of items, we can query from the python using:
```
items = Item.query.all()
```
We can use [SQLite browser](https://sqlitebrowser.org/) software to get graphical interface of the database.

### Resturucture the files
We can separate the routes and database models with difference files to get clear structure. So, all the routes are placed in `routes.py` file and database is in `models.py` file.

We need to create a package structure to run automatically as a python package. The structure should be: (main file **market.py** is deleted and move to code to respective files.)
```
main_folder
    |___market_package
    |       |___templates_folder
    |       |       |___(with templates htmls)
    |       |___(__init__.py)
    |       |___market.db
    |       |___models.py
    |       |___routes.py
    |___run.py
```
We can easily run the web app with `python run.py`.
```
<!-- run.py -->
from market import app # (market --> market_package)
if __name__ == '__main__':
    app.run(debug=True)
```

```
<!-- __init__.py (initialize the flask web) -->
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # database conversion library

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

from market import routes
```

```
<!-- routes.py (put all the decorators and routes in this file) -->
from market import app
from market.models import Item
from flask import render_template

@app.route("/home")
def home_page():
    return render_template('home.html')
```
```
<!-- models.py -->
from market import db

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # limiting the length of string, cannot be blank, cannot be same name
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item{self.name}'
```

We can create new database by adding database class in `models.py`. Added `User` table and edited `Item` table is:
```
from market import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    # password will be store with hashing
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000) # when register, it will initialize with 1000
    # relational to Item table
    items = db.relationship('Item', backref='owned_user', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # limiting the length of string, cannot be blank, cannot be same name
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item{self.name}'
```
We can add data via python shell which should launch in root location (`main_folder`).
```
>>> from market.models import db
>>> db.drop_all()       # delete all db since create new table and add new field at previous table (this dropping is optional)
>>> db.create_all()
>>> from market.models import User, Item
>>> u1 = User(username='Min', email='min@min.com', password_hash='9248115713')
>>> db.session.add(u1)
>>> db.session.commit()
>>> User.query.all()

>>> i1 = Item(name='iPhone 12', description='New iPhone', barcode='837931741063', price=900)
>>> db.session.add(i1)
>>> db.session.commit()
>>> i2 = Item(name='iPhone 12 Pro', description='New iPhone Pro', barcode='837931741164', price=1050)
>>> db.session.add(i2)
>>> db.session.commit()

>>> item1 = Item.query.filter_by(name='iPhone 12').first()
>>> db.session.add(item1)
>>> db.session.commit()     # this can be errored since we defined by user.id at owner field
>>> db.session.rollback()
>>> item1.owner = User.query.filter_by(username='Min').first().id
>>> db.session.add(item1)
>>> db.session.commit()
>>> item1.owner             # should return id

>>> i = Item.query.filter_by(name='iPhone 12').first()
>>> i.owned_user            # should return user_id (since backref=owned_user)

```

### Create user data via web app
Flask supports form-packages to use with **HTML** template. These packages can be installed as:
`$ pip install flask-wtf`
`$ pip install wtforms`

To show up the form in **HTML**, secret key will be required for a security layer. That key can be generated from python shell. That key can be initialized in `__init__.py` as `app.config['SECRET_KEY'] = '<generated_key>'`
```
>>> import os
>>> os.urandom(12).hex()        # 59082d3e65e110369a9b3a3e
```
Forms format should be stored in `forms.py` and the route can be create via `routes.py`.
```
<!-- routes.py -->
from market.forms import RegisterForm

@app.route('/register')
def register_page():
   form = RegisterForm()
   return render_template('register.html', form=form) # html have to be created
```
```
<!-- forms.py -->
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField(label='User Name')
    email = StringField(label='Email Address:')
    # for registeration, confirmation password will need
    password1 = PasswordField(label='Password')
    password2 = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Create Account')
```

Need to allow the route to handle the request.

When data sending from client to server, one of the most known attack is CSRF which stole data from database.

`$ pip install flask_bcrypt`: use for hashing password.
`$ pip install flask_login`: allow the login system easily with flask.

We can differentiate that the user is logged in or not. We can implement using `Jinja` syntex how to the **HTML** page is look like when login and not login. Previously installed `flask_login` package handle the session for user login.
```
{% if current_user.is_authenticated %}
    <!-- HTML when login -->
{% else %}
    <!-- HTML before login -->
{% endif %}
```

We can do sperate **HTML** to avoid messy. So that, create a new **HTML** and this can be include by `{% include '<location>/<filename>.html' %}`. Modal have `id` and so we can reference the model where we need.
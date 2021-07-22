from market import app
from market.models import Item, User
from flask import render_template, redirect, url_for, flash, request
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db   # since it located in __init__.py
from flask_login import login_user, logout_user, login_required, current_user

from colorama import init, Fore  # print color
init(autoreset=True)

@app.route("/") # Decorators for the route function (routing to a page)
@app.route("/home")
def home_page():
    return render_template('home.html') # located in templates folder
# render_template() knows how to handle requests and direct into html files

# send data from this route to html
@app.route('/market', methods=['GET', 'POST'])
@login_required # check before rendering market_page
def market_page():
    # after creating database, these item list are added to db using python shell script
    # then these are query using --> Item.query.all()
    # items_list = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    # testing about the info
    # if purchase_form.validate_on_submit(): 
    #     print(purchase_form) # will give object of form <market.forms.PurchaseItemForm object at 0x7fa798656c40>
    #     print(purchase_form.__dict__) # will give more info fields
    #     print(purchase_form['submit']) # to get information about submittings
    #     print(request.form.get('purchased_item')) # will get item.name
    if request.method == 'POST':
        # Purchase Item Logic
        purchase_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchase_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object): # check the budget (within User model)
                """ below three line are moved to Item model
                p_item_object.owner = current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()
                """
                p_item_object.buy(current_user)
                print(Fore.GREEN + f"Congrarulation! You purchased {p_item_object.name} for $ {p_item_object.price}")
                flash(f"Congrarulation! You purchased {p_item_object.name} for $ {p_item_object.price}", category='success')
            else:
                print(Fore.RED + f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!")
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                print(Fore.GREEN + f"Congrarulation! You sold {s_item_object.name} back to market!")
                flash(f"Congrarulation! You sold {s_item_object.name} back to market with!", category='success')
            else:
                print(Fore.RED + f"Something went wrong with selling {s_item_object.name}!")
                flash(f"Something went wrong with selling {s_item_object.name}!", category='danger')
        return redirect(url_for('market_page'))
    
    if request.method == 'GET':
        items_list = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id) # query the current user's items
        return render_template('market.html', 
                                items=items_list, 
                                purchase_form=purchase_form, 
                                owned_items=owned_items, 
                                selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit(): # check all info is valid and on_submit
        # SQLAlchemy db script
        user_to_create = User(username=form.username.data,
                                email = form.email.data,
                                password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        # after registering, we want the user to login automatically
        login_user(user_to_create)
        print(Fore.GREEN + f'Account created successfully! You are now logged in as: {user_to_create.username}')
        flash(f'Account created successfully! You are now logged in as: {user_to_create.username}', category='success')        

        return redirect(url_for('market_page')) # expect URL

    if form.errors != {}: # if no error from validation
        for err_msg in form.errors.values():
            print(Fore.RED + f'ERROR: {err_msg[0]}')
            flash(f'ERROR: {err_msg[0]}', category='danger') # printing error messages at HTML
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit(): # check all info is valid and on_submit
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            print(Fore.GREEN + f'Success! You are logged in as: {attempted_user.username}')
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            print(Fore.RED + f'ERROR: Username and Password are not match! Please try again.')
            flash(f'Username and Password are not match! Please try again.', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    print(Fore.YELLOW + f'You have bee looged out!')
    flash(f'[!] You have bee looged out!', category='info')
    return redirect(url_for('home_page'))


# -------------------------------------------------
# -------------------------------------------------
# static route
@app.route("/about")
def about_page():
    return '<h1>About Page</h1>'

# dynamic route (<name> and function parsing must same)
@app.route("/about/<username>")
def about_page_user(username):
    return f'<h1>This is about the page of {username}</h1>'


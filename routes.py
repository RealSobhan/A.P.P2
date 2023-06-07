from flask import render_template, request, redirect, url_for, session
from app import app
import pandas as pd
from utils import create_csv, csv_to_dict, correct_link, get_currency

# creating an initial csv as a database to read a one
try:
    products = pd.read_csv("warehouse.csv")
except FileNotFoundError:
    create_csv(f"warehouse", ["name", "price", "drive_link"])
    products = pd.read_csv("warehouse.csv")

# route for our home page
@app.route('/', methods=['GET', 'POST'])
def index():
    product_to_show = csv_to_dict("warehouse.csv")
    for product in product_to_show:
        product["price"] = float(product["price"])
    return render_template('products.html', products=product_to_show, exchange_rate=int(get_currency() * 10), title="Home")

# route for admin panel that can only add item
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global products  # Declare the variable as global

    if request.method == 'POST':
        # Add new item to the database
        new_row = pd.DataFrame({'name': [request.form['name']], "price": [float(request.form['price'])], "drive_link": [correct_link(request.form['image'])]})
        products = pd.concat([products, new_row], ignore_index=True)
        products.to_csv('warehouse.csv', index=False)
        products = pd.read_csv("warehouse.csv")

    return render_template('admin.html', title="Admin panel") 

@app.route('/remove_from_warehouse', methods=['GET', 'POST'])
def remove_from_warehouse():
    global products  # Declare the variable as global to have access to the database that have been created outside of the def

    if request.method == 'POST':
        products = products[products["name"] != request.form['name']]
        products.to_csv('warehouse.csv', index=False)
        products = pd.read_csv("warehouse.csv")
    return render_template('admin.html', title="Admin panel") 


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    name = request.form['name']
    price = float(request.form['price'])
    image = request.form['image']
    product = {'name': name, 'price': price, 'image': image}
    
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product)
    session.modified = True  # Save the session after modifying the cart
    
    return redirect(url_for('cart'))


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    name = request.form['name']
    
    cart_items = session.get('cart', [])
    new_cart = []
    
    for item in cart_items :
        if item['name'] != name:
            new_cart.append(item)
        else:
            continue
        
    cart_items = new_cart
    
    session['cart'] = cart_items
    session.modified = True  # Save the session after modifying the cart
    
    return redirect(url_for('cart'))



@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items) if cart_items else 0 # Calculate the total price of the cart
    exchange_rate = int(get_currency() * 10)
    total_price_rials = int(total_price * exchange_rate) # exchange rate is the ratio between USD and Rials
    return render_template('cart.html', cart=cart_items, total_price=total_price,
                           total_price_rials=total_price_rials, exchange_rate=exchange_rate, title="Cart")

@app.route('/edit_cart_quantity', methods=['POST'])
def edit_cart_quantity():
    name = request.form['name']
    price = float(request.form['price'])
    image = request.form['image']
    cart_items = session.get('cart', [])
    
    new_quantity = int(request.form['new_quantity'])
    print(cart_items)
    # first we count the difference between current amount of the product in our cart and the amount we want:
    counter = 0
    for item in cart_items :
        if item['name'] == name :
            counter += 1
    
    # we create a dictionary that is in the format of edited product:
    d = {'name':name, 'price':price, 'image':image}    
    new_cart = []
    
    for item in cart_items :
        if item['name'] != name:
            new_cart.append(item)
        else:
            continue
        
    for i in range(new_quantity):
        new_cart.append(d)
    
    cart_items = new_cart
    
    session['cart'] = cart_items
    session.modified = True  # Save the session after modifying the cart
    return redirect(url_for('cart'))


@app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
    session['cart'] = []
    session.modified = True  # Save the session after modifying the cart
    return render_template('purchase_confirmation.html', title="Purchase Confirmed")

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global products  # Declare the variable as global

    if request.method == 'POST':
        new_row = pd.DataFrame({'name': [request.form['name']], "price": [float(request.form['price'])], "drive_link": [correct_link(request.form['image'])]})
        products = pd.concat([products, new_row], ignore_index=True)
        products.to_csv('warehouse.csv', index=False)
        products = pd.read_csv("warehouse.csv")

    return render_template('admin.html') 

@app.route('/remove_from_warehouse', methods=['GET', 'POST'])
def remove_from_warehouse():
    global products  # Declare the variable as global

    if request.method == 'POST':
        products = products[products["name"] != request.form['name']]
        products.to_csv('warehouse.csv', index=False)
        products = pd.read_csv("warehouse.csv")
    return render_template('admin.html') 

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



@app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
    session['cart'] = []
    session.modified = True  # Save the session after modifying the cart
    return render_template('purchase_confirmation.html')

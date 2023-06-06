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
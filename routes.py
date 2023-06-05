from flask import render_template
from app import app
import pandas as pd



# creating an initial csv as a database ro read a one
try:
    products = pd.read_csv("warehouse.csv")
except FileNotFoundError:
    create_csv(f"warehouse", ["name", "price", "drive_link"])
    products = pd.read_csv("warehouse.csv")
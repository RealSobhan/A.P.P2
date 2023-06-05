from flask import Flask
from config import Config

# create the base of the back
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)

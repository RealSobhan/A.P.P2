from flask import Flask
from flask_session import Session
from config import Config

# create the base of the back
app = Flask(__name__)
app.config.from_object(Config)
Session(app)


if __name__ == '__main__':
    app.run(debug=True)

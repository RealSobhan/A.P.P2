import secrets

#setting configs that is needed to run the app
class Config:
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = secrets.token_hex(16)
    SESSION_FILE_DIR = './.flask_session/'

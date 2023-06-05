import secrets

#setting configs that is needed to run the app
class Config:
    SECRET_KEY = secrets.token_hex(16)


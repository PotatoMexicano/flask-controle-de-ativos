from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.ext.declarative
from flask_qrcode import QRcode
from flask_login.login_manager import LoginManager
from decouple import config
import pathlib
# from flask_qrcode import QRcode

# Recebe as váriaveis globais
config.encoding = 'cp1251'
SECRET_KEY = config('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
COMPANY_NAME = config('COMPANY_NAME')

# Inicia a instancia aplicativo
app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['COMPANY_NAME'] = COMPANY_NAME
app.config['JSON_AS_ASCII'] = False

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

QRcode(app)
login_manager = LoginManager(app)


from app.routes.auth.routes import auth_routes
from app.routes.homepage.routes import home_routes
from app.routes.logistic.routes import logistic_routes

app.register_blueprint(auth_routes)
app.register_blueprint(home_routes)
app.register_blueprint(logistic_routes)

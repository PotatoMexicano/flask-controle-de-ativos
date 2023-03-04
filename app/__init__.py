from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.ext.declarative
from flask_qrcode import QRcode
from flask_login.login_manager import LoginManager
from decouple import config
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

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

QRcode(app)
login_manager = LoginManager(app)


from app.routes.auth.routes import auth_routes

app.register_blueprint(auth_routes)


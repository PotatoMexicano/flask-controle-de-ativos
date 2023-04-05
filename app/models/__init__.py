from app import app, db, login_manager
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Time, Boolean, select, update, insert, ForeignKey
from werkzeug.datastructures import ImmutableMultiDict
from sqlalchemy.orm import Session, column_property, reconstructor
from flask_login import UserMixin
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import locale

session:Session = db.session

@dataclass
class LogisticCenter(db.Model):

    __tabelname__ = 'logistic_center'
    __allow_unmapped__ = True

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(45), unique=True, nullable=False)
    
    zipcode:str = Column(String(20), nullable=True)
    address:str = Column(String(55), nullable=False)
    district:str = Column(String(30), nullable=False)
    city:str = Column(String(30), nullable=False)
    state:str = Column(String(30), nullable=False)
    country:str = Column(String(30), nullable=False)
    fullAddress:str = column_property(address + " - " + district + ", " + city + ", " + state + ", " + country + ", " + zipcode)
    phoneOne:str = Column(String(20), nullable=False)
    phoneTwo:str = Column(String(20), nullable=True)
    email:str = Column(String(45), nullable=False)
    enabled:bool = Column(Boolean, nullable=False, default=True)
    createAt:datetime = Column(DateTime, nullable=False, default=datetime.now)
           
    def __repr__(self) -> str:
        return f'<LogisticCenter: {self.name}>'
    
    def create(self) -> dict:

        if LogisticCenter.list_one(name = self.name):
            return {'status': False, 'message': 'Object already exist.'}
        
        try:
            
            session.add(self)
            session.commit()
            session.refresh(self)
            
            return {'status': True, 'message': 'Success'}
        
        except Exception as stderr:

            return {'status': False, 'message': str(stderr)}

    def update(self, form:ImmutableMultiDict):

        try:
            for campo, valor in form.items():
                setattr(self, campo, valor)

            session.commit()
            session.refresh(self)
            return self
        except:
            return None

    def list_one(id:int = None, name:str = None):

        if not id and not name:
            return 'endpoint needs [id, name] for search.'

        id = int(id) if str(id).isdigit() else None

        if id:
            raw = select(LogisticCenter).where(LogisticCenter.id == id)
        
        if name:
            raw = select(LogisticCenter).where(LogisticCenter.name == name)

        response = session.execute(raw).scalar_one_or_none()

        if not response:
            return None
            
        return response
    
    def list_all():

        raw = select(LogisticCenter).order_by(LogisticCenter.id)
        response = session.execute(raw).scalars().all()

        if not response:
            return None

        return response

@dataclass
class Product(db.Model):
    __tabelname__ = 'logistic_center'
    __allow_unmapped__ = True

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    
    name:str = Column(String(255), unique=True, nullable=False)
    model:str = Column(String(255), nullable=False)
    serieNumber:str = Column(String(255), nullable=True)
    manufacturer:str = Column(String(255), nullable=False)
    price:float = Column(Float, nullable=False)
    observation:str = Column(String(255), nullable=True)    
    createAt:datetime = Column(DateTime, nullable=False, default=datetime.now)

    priceStr:str = None

    def __init__(self, name:str, model:str, serieNumber:str, manufacturer:str, price:float, observation:str = None) -> None:

        self.name = name
        self.model = model
        self.serieNumber = serieNumber
        self.manufacturer = manufacturer
        self.price = price
        self.observation = observation
        
    def __repr__(self) -> str:
        return f"<Product: id({self.id})>"

    def gen_fields(self):

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        self.priceStr = locale.currency(self.price, grouping=True, symbol=True)

        return self

    def create(self) -> dict:

        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return {'status': True, 'message': 'Success'}
        except Exception as stderr:
            return {'status': False, 'message': str(stderr)}

    def update(self, form:ImmutableMultiDict):

        try:
            for campo, valor in form.items():
                setattr(self, campo, valor)

            session.commit()
            session.refresh(self)
            return self
        except:
            return None

    def list_one(id:int = None):

        if not id:
            return 'endpoint needs [id] for search.'

        id = int(id) if str(id).isdigit() else None

        if id:
            raw = select(Product).where(Product.id == id)
        
        response = session.execute(raw).scalar_one_or_none()

        if not response:
            return None
            
        return response

    def list_all():

        raw = select(Product).order_by(Product.id)
        response = session.execute(raw).scalars().all()

        response = [resp.gen_fields() for resp in response]

        if not response:
            return None

        return response

@dataclass
class User(db.Model, UserMixin):

    __tablename__ = 'users'
    __allow_unmapped__ = True

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    login:str = Column(String(25), unique=True, nullable=False)
    email:str = Column(String(80), unique=True, nullable=True)
    fullName:str = Column(String(100), nullable=False)
    password = Column(String(60), nullable=False)
    enabled:bool = Column(Boolean, nullable=False, default=True)
    enabled2FA:bool = Column(Boolean, nullable=False, default=False)
    secret2FA:str = Column(String(32), nullable=True)
    createAt:datetime = Column(DateTime, nullable=False, default=datetime.now)
    loginAt:datetime = Column(DateTime, nullable=True)

    logistic_centers:list = None

    @reconstructor
    def init_on_load(self):
        self.logistic_centers:list = []

    def __repr__(self) -> str:
        return f'<User: {self.login}>'

    def generate_2FA(self) -> str:
        import pyotp
        token = pyotp.random_base32()
        return token

    def view_2FA_QRCode(self):
        import pyotp
        token = pyotp.totp.TOTP(self.secret2FA).provisioning_uri(name=f'{self.login}', issuer_name= str('Controle de ativos 3.0'))
        return str(token)

    def update_2FA(self, token:str) -> bool:
        self.secret2FA = str(token)
        session.commit()

    def update_loginAt(self) -> None:
        self.loginAt = datetime.now()
        session.commit()

    def validate_2FA(self, userInput:int) -> bool:
        import pyotp
        return pyotp.TOTP(self.secret2FA).verify(int(userInput))

    def create(self) -> bool:
        try:
        
            session.add(self)
            session.commit()
            session.refresh(self)
            return True
        
        except Exception as stderr:
            print(f"STDERR -> {stderr}")
            return False

    @login_manager.user_loader
    def list_one(id:int = None, login:str = None, email:str = None):

        if not login and not id and not email:
            return 'endpoint needs [login, id, email] for search.'

        if id:
            raw = select(User).where(User.id == id)
        
        if login:
            raw = select(User).where(User.login == login)
        
        if email:
            raw = select(User).where(User.email == email)

        response = session.execute(raw).scalar_one_or_none()

        if not response:
            return None
        
        return response

    def split(self) -> tuple:
        
        user_fullName_splited = str(self.fullName).split(' ')

        firstName = user_fullName_splited[0][0]
        lastName = user_fullName_splited[-1][0]

        if len(user_fullName_splited) == 1:
            lastName = ''

        return firstName, lastName
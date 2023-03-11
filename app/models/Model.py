from app import app, db, login_manager
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Time, Boolean, select, update, insert
from sqlalchemy.orm import Session, column_property, reconstructor
from flask_login import UserMixin
from dataclasses import dataclass, asdict, field
from datetime import datetime

session:Session = db.session

@dataclass
class Tag(db.Model):

    __tabelname__ = 'tag'
    __allow_unmapped__ = True

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(10), unique=True, nullable=False)
    enabled:bool = Column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f'<Tag: {self.name}>'
    
    def create(self) -> bool:
        try:
        
            session.add(self)
            session.commit()
            session.refresh(self)
            return True
        
        except Exception as stderr:
            print(f"STDERR -> {stderr}")
            return False

    def list_one(id:int = None, name:str = None):

        if not id and not name:
            return 'endpoint needs [id, name] for search.'

        if id:
            raw = select(Tag).where(Tag.id == id)

        if name:
            raw = select(Tag).where(Tag.name == name)
        
        response = session.execute(raw).scalar_one_or_none()

        if not response:
            return None
        
        return response
    
    def list_all():

        raw = select(Tag)
        response = session.execute(raw).scalars().all()

        if not response:
            return None
        
        return response

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

    tags:list = None
        
    @reconstructor
    def init_on_load(self):
        self.tags:list = []
    
    def __repr__(self) -> str:
        return f'<LogisticCenter: {self.name}>'
    
    def create(self) -> bool:
        try:
        
            session.add(self)
            session.commit()
            session.refresh(self)
            return True
        
        except Exception as stderr:
            print(f"STDERR -> {stderr}")
            return False

    def list_one(id:int = None, tags:bool = False):

        if not id:
            return 'endpoint needs [id] for search.'

        if id:
            raw = select(LogisticCenter).where(LogisticCenter.id == id)
        
        response = session.execute(raw).scalar_one_or_none()

        if not response:
            return None
        
        if tags:
            response = [r.load_tags() for r in response]
            
        return response
    
    def list_all(tags:bool = False):

        raw = select(LogisticCenter)
        response = session.execute(raw).scalars().all()

        if not response:
            return None
        
        if tags:
            response = [r.load_tags() for r in response]
        
        return response

    def load_tags(self):
        
        self.tags.append('Tag #1')
        self.tags.append('Tag #2')
    
        return self

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

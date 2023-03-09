from app import app, db, login_manager
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Time, Boolean, select, update, insert
from sqlalchemy.orm import Session
from flask_login import UserMixin
from dataclasses import dataclass, asdict
from datetime import datetime

session:Session = db.session

@dataclass
class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    login:str = Column(String(25), unique=True, nullable=False)
    email:str = Column(String(80), unique=True, nullable=True)
    fullName:str = Column(String(100), nullable=False)
    password = Column(String(60), nullable=False)
    admin_role = Column(Boolean, nullable=False, default=False)
    enabled:bool = Column(Boolean, nullable=False, default=True)
    enabled2FA:bool = Column(Boolean, nullable=False, default=False)
    secret2FA:str = Column(String(32), nullable=True)
    createAt:datetime = Column(DateTime, nullable=False, default=datetime.now)
    loginAt:datetime = Column(DateTime, nullable=True)

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
    def listOne(id:int = None, login:str = None, email:str = None):

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

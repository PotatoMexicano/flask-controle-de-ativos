from app import app, db, login_manager
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Time, Boolean, select, update
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
    fullName:str = Column(String(100), nullable=False)
    password = Column(String(60), nullable=False)
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

    def validate_2FA(self, userInput:int) -> bool:
        import pyotp
        return pyotp.TOTP(self.secret2FA).verify(int(userInput))
    
    @login_manager.user_loader
    def listOne(id:int = None, login:str = None):

        if not login and not id:
            return 'endpoint needs [login, id] for search.'

        if id:
            raw = select(User).where(User.id == id)
        
        if login:
            raw = select(User).where(User.login == login)

        response = session.execute(raw).scalar_one_or_none()

        if not response:
            return None
        
        return response

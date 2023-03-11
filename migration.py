from app import app, db
from app.models.Model import User
from app.models.Model import LogisticCenter
from app.models.Model import Tag
from sqlalchemy.orm import Session

session: Session = db.session
with app.app_context():

    db.drop_all()
    db.create_all()

    user = User(
        login='gabriel',
        fullName='Gabriel',
        email='gabriel@email.com',
        password='$2a$12$y0VTmEq1E/c1urez1TPxAOxwNM7L1pqC6t.gVWdBmvug/EtZaNYeq',
        secret2FA='LNO4TJILQXOTMILOVTFSV2AWUYIP5RSP',
        enabled=True,
        enabled2FA=True
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #1',
        zipcode='13417001',
        address='Rua 25 de julho, 1823',
        district='Colinas',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970623',
        phoneTwo='+55 (19) 34267291',
        email='logistic_01_potato@email.com'
    ).create()
    
    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #2',
        zipcode='13417002',
        address='Rua 26 de julho, 1823',
        district='Colinas',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970624',
        phoneTwo='+55 (19) 34267292',
        email='logistic_02_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #3',
        zipcode='13417003',
        address='Rua 27 de julho, 1823',
        district='Colinas',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970625',
        phoneTwo='+55 (19) 34267295',
        email='logistic_03_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #4',
        zipcode='13417004',
        address='Rua 28 de julho, 1823',
        district='Colinas',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_04_potato@email.com'
    ).create()

    tag = Tag(name='Tag#01').create()
    tag = Tag(name='Tag#02').create()
    tag = Tag(name='Tag#03').create()
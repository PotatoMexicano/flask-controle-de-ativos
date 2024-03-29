from app import app, db
from app.models import User
from app.models import LogisticCenter
from app.models import Product
from sqlalchemy.orm import Session

session: Session = db.session
with app.app_context():

    db.drop_all()
    db.create_all()

    user = User(
        login='gabriel',
        fullName='Gabriel Antonio Cordeiro',
        email='gabriel@email.com',
        password='$2a$12$y0VTmEq1E/c1urez1TPxAOxwNM7L1pqC6t.gVWdBmvug/EtZaNYeq',
        secret2FA='LNO4TJILQXOTMILOVTFSV2AWUYIP5RSP',
        enabled=True,
        enabled2FA=True
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #1',
        zipcode='13417001',
        address='Rua Riachuelo, 1390',
        district='Centro',
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
        address='Rua Riachuelo, 1391',
        district='Centro',
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
        address='Rua Riachuelo, 1392',
        district='Centro',
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
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_04_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #5',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_05_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #6',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_06_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #7',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_07_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #8',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_08_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #9',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_09_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #10',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_10_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #11',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_11_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #12',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_12_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #13',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_13_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #14',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_14_potato@email.com'
    ).create()

    logistic_center = LogisticCenter(
        name='Centro logistico Piracicaba #15',
        zipcode='13417004',
        address='Rua Riachuelo, 1393',
        district='Centro',
        city='Piracicaba',
        state='São Paulo',
        country='Brazil',
        phoneOne='+55 (19) 998970626',
        phoneTwo='+55 (19) 34267296',
        email='logistic_15_potato@email.com'
    ).create()

    product = Product(
        name='Teclado sem fio',
        manufacturer='Logitech',
        model='NK0192-2023',
        price=129.99,
        serieNumber='24287234'
    ).create()

    product = Product(
        name='Mouse sem fio',
        manufacturer='Logitech',
        model='NK0132-2023',
        price=51.99,
        serieNumber='2428712AA'
    ).create()

    product = Product(
        name='Monitor Dell FHD',
        manufacturer='Dell',
        model='DELL102-2023',
        price=1029.99,
        serieNumber='IWHFD822',
        observation='1920x1080 144hz 1ms IPS'
    ).create()
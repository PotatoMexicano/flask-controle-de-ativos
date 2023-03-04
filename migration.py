from app import app, db
from app.models.Model import User
from sqlalchemy.orm import Session

session:Session = db.session
with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(
        login = 'gabriel',
        fullName = 'Gabriel',
        password = '$2a$12$y0VTmEq1E/c1urez1TPxAOxwNM7L1pqC6t.gVWdBmvug/EtZaNYeq',
        enabled = True,
        enabled2FA = True
    )
    
    user.update_2FA(user.generate_2FA())

    session.add(user)
    session.commit()
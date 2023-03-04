from flask import Blueprint, render_template, render_template_string, url_for, request, flash, redirect, session as flaskSession
from app.models.Model import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Field
from wtforms.validators import InputRequired, Length
from flask_login import login_user, logout_user, current_user
import bcrypt

class LoginForm(FlaskForm):
    
    username = StringField('Your username', validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField('Your password', validators=[InputRequired(), Length(min=8, max=64)])
    remember_me = BooleanField('Keep me logged in', default='y')
    submit = SubmitField('Log In')

auth_routes = Blueprint(name='auth', import_name=__name__, template_folder='template', url_prefix='/auth')

def middleware(fallback, user:User):
    
    if user.enabled2FA: #if user has 2FA enabled
        
        flaskSession['2FA_USER'] = user.login

        return redirect(url_for('auth.two_fa_validation'))
    
    else: # if user has'nt 2FA enabled

        login_user(user)
        return render_template_string(f'<h1>Welcome {user.fullName}</h1>')

@auth_routes.route('/2FA', methods=['GET','POST'])
def two_fa_validation():
    login_username = flaskSession['2FA_USER']
    user = User.listOne(login = login_username)

    if request.method == 'GET':
        return render_template('2FA.html', data={'title':'2FA', 'qrcode': str(user.view_2FA_QRCode()) })
    
    if request.method == 'POST':
        
        number1 = int(request.form.get('number1'))
        number2 = int(request.form.get('number2'))
        number3 = int(request.form.get('number3'))
        number4 = int(request.form.get('number4'))
        number5 = int(request.form.get('number5'))
        number6 = int(request.form.get('number6'))
        
        numberFull = int("".join([str(number1), str(number2), str(number3), str(number4), str(number5), str(number6)]))

        if user.validate_2FA(numberFull):
            print("OK")
        else:
            print("NOT OK")

        login_user(user)
        return render_template_string(f'<h1>Welcome {user.fullName}</h1>')

@auth_routes.route('/login', methods=['GET','POST'])
def auth_user():
    
    if request.method == 'GET':

        form = LoginForm()
        if form.validate_on_submit(): return render_template('login.html')
        data = {'title': 'Login'}
        return render_template('login.html', data=data, form=form)
    
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        remember = (True if request.form.get('remember_me') == 'y' else False)

        user:User = User.listOne(login = username)

        if user:

            if bcrypt.checkpw(str(password).encode(), str(user.password).encode()):

                return middleware(fallback=url_for('auth.auth_user'), user=user)
                        
            flash(f"Invalid credentials.", "error")
            return redirect(url_for('auth.auth_user'))
                

        flash(f"Invalid credentials.", "error")
        return redirect(url_for('auth.auth_user'))

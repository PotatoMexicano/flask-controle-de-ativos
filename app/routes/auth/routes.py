from flask import Blueprint, render_template, url_for, request, flash, redirect, session as flaskSession
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
        flaskSession['2FA_AUTHENTICATION'] = True

        return redirect(url_for('auth.two_fa_validation'))
    
    else: # if user has'nt 2FA enabled

        login_user(user, remember=flaskSession.get('USER_REMEMBER'))
        return redirect(url_for('homepage.homepage'))

@auth_routes.route('/2FA', methods=['GET','POST'])
def two_fa_validation():
    
    if not flaskSession.get('2FA_USER'):
        # Redirect user to login if session not exists
        flash('Login required', 'error')
        return redirect(url_for('auth.auth_user'))
    
    login_username = flaskSession['2FA_USER']
    user = User.listOne(login = login_username)
    # Find user object using session 

    if request.method == 'GET':
        # If request is GET, render 2FA page
        # return render_template('2FA.html', data={'title':'2FA', 'qrcode': str(user.view_2FA_QRCode()) })

        if not flaskSession.get('2FA_AUTHENTICATION'):
            return redirect(url_for('homepage.homepage'))
        
        return render_template('2FA.html', data={'title':'2FA'})
        
    
    if request.method == 'POST':
        # If request is POST, get data from form
        number1 = int(request.form.get('number1'))
        number2 = int(request.form.get('number2'))
        number3 = int(request.form.get('number3'))
        number4 = int(request.form.get('number4'))
        number5 = int(request.form.get('number5'))
        number6 = int(request.form.get('number6'))
        
        # concate all the six numbers in one
        numberFull = int("".join([str(number1), str(number2), str(number3), str(number4), str(number5), str(number6)]))

        if user.validate_2FA(numberFull):
            # the code inputed by user was valid, redirect to homepage
            flaskSession['2FA_AUTHENTICATION'] = False
        else:
            # the code inputed by user was not valid, redirect to 2FA page again
            flash("Invalid token","error")
            return redirect(url_for('auth.two_fa_validation'))

        login_user(user, remember=flaskSession.get('USER_REMEMBER'))
        return redirect(url_for('homepage.homepage'))

@auth_routes.route('/login', methods=['GET','POST'])
def auth_user():
    
    if request.method == 'GET':

        # Check if this alternative is viable, idk if keep it
        # if flaskSession.get('2FA_AUTHENTICATION') == True:
        #     return redirect(url_for('auth.two_fa_validation'))

        form = LoginForm()
        if form.validate_on_submit(): return render_template('login.html')
        data = {'title': 'Login'}
        return render_template('login.html', data=data, form=form)
    
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        flaskSession['USER_REMEMBER'] = (True if request.form.get('remember_me') == 'y' else False)

        user:User = User.listOne(login = username)

        if user:

            if bcrypt.checkpw(str(password).encode(), str(user.password).encode()):

                return middleware(fallback=url_for('auth.auth_user'), user=user)
                        
            flash(f"Invalid credentials.", "error")
            return redirect(url_for('auth.auth_user'))
                

        flash(f"Invalid credentials.", "error")
        return redirect(url_for('auth.auth_user'))

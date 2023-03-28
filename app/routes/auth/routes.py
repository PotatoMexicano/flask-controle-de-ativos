from flask import Blueprint, render_template, url_for, request, flash, redirect, session as flaskSession, jsonify
from app.models.Model import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_login import login_user, logout_user, current_user
import bcrypt

class LoginForm(FlaskForm):
    
    username = StringField('Your username', validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "Jose@Silva.com"})
    password = PasswordField('Your password', validators=[InputRequired(), Length(min=8, max=64)], render_kw={"placeholder": "Your strong password"}, id='InputPassword')
    remember_me = BooleanField('Keep me logged in', default='')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):

    username = StringField('Your username', validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "Jose Silva"})
    fullName = StringField('Your fullname', validators=[InputRequired(), Length(min=10, max=30)], render_kw={"placeholder": "José da Silva Souza"})
    email = StringField('Your email', validators=[InputRequired(), Length(min=8, max=80)], render_kw={"placeholder": "Jose@Silva.com"})
    password = PasswordField('Your password', validators=[InputRequired(), Length(min=8, max=64)], render_kw={"placeholder": "Your strong password"}, id='InputPassword')
    submit = SubmitField('Register')

auth_routes = Blueprint(name='auth', import_name=__name__, template_folder='../templates', url_prefix='/auth')

def middleware(fallback, user:User):
    
    if user.enabled2FA: #if user has 2FA enabled
        
        flaskSession['2FA_USER'] = user.login
        flaskSession['2FA_AUTHENTICATION'] = True

        return redirect(url_for('auth.two_fa_validation'))
    
    else: # if user has'nt 2FA enabled

        login_user(user, remember=flaskSession.get('USER_REMEMBER'))
        user.update_loginAt()
        return redirect(url_for('homepage.homepage'))

@auth_routes.route('/2FA', methods=['GET','POST'])
def two_fa_validation():
    
    if not flaskSession.get('2FA_USER'):
        # Redirect user to login if session not exists
        flash('Login required', 'error')
        return redirect(url_for('auth.auth_user'))
    
    login_username = flaskSession['2FA_USER']
    user = User.list_one(login = login_username)
    # Find user object using session 

    if request.method == 'GET':
        # If request is GET, render 2FA page
        # return render_template('auth/2FA.html', data={'title':'2FA', 'qrcode': str(user.view_2FA_QRCode()) })

        if not flaskSession.get('2FA_AUTHENTICATION'):
            return redirect(url_for('homepage.homepage'))
        
        return render_template('auth/2FA.html', data={'title':'2FA', 'qrcode': str(user.view_2FA_QRCode())})
        
    
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
        # if all its ok, auth user into system and redirect them to homepage

        user.update_loginAt()
        return redirect(url_for('homepage.homepage'))

@auth_routes.route('/login', methods=['GET','POST'])
def auth_user():
    
    if request.method == 'GET':

        resetPassword = False
        # starts resetPassword with False

        if flaskSession.get('USER_TRY_LOGIN'):
            # checks if global exists
            if flaskSession.get('USER_TRY_LOGIN') >= 3:
                # if counter is more than 3, show alert for change password
                resetPassword = True
                flaskSession['USER_TRY_LOGIN'] = 0
                # reset counter

        form = LoginForm()
        if form.validate_on_submit(): return render_template('auth/login.html')
        data = {'title': 'Login'}
        return render_template('auth/login.html', data=data, form=form, resetPassword=resetPassword)
    
    if request.method == 'POST':

        if not flaskSession.get('USER_TRY_LOGIN'): flaskSession['USER_TRY_LOGIN'] = 0
        # If the var does not exists, create one with initial value zero.

        username = request.form.get('username')
        password = request.form.get('password')
        flaskSession['USER_REMEMBER'] = (True if request.form.get('remember_me') == 'y' else False)
        # receive from front-end values inserted in inputs

        def find_emails(text):
            import re
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(pattern, text)
            return emails

        emails:list = find_emails(username)
        # Check if input's user is an email (using regex for check this)
        
        if len(emails) >= 1:
            user:User = User.list_one(email = username)
            # if regex finds one or more emails in the string, try login with this

        else:
            user:User = User.list_one(login = username)
            # else, try like a login

        if user:
            # if the user was found in database, check your password

            if bcrypt.checkpw(str(password).encode(), str(user.password).encode()):

                return middleware(fallback=url_for('auth.auth_user'), user=user)
                #redirect user to middleware for check if 2FA is enabled
                        
            flaskSession['USER_TRY_LOGIN'] += 1
            # case if the user insert wrong password, add 1 to counter

            flash(f"Invalid credentials.", "error")
            return redirect(url_for('auth.auth_user'))
            # redirect user to login page again

        flash(f"Invalid credentials.", "error")
        return redirect(url_for('auth.auth_user'))
        # redirect user to login page again

@auth_routes.route('/register', methods=['GET','POST'])
def register_user():

    if request.method == 'GET':

        form = RegisterForm()
        if form.validate_on_submit(): return render_template('auth/register.html')
        data = {'title': 'Register'}
        return render_template('auth/register.html', data=data, form=form)
        # render the register form

    if request.method == 'POST':

        username = str(request.form.get('username')).lower()
        fullName = str(request.form.get('fullName'))
        email = str(request.form.get('email'))
        password = bcrypt.hashpw(str(request.form.get('password')).encode(), bcrypt.gensalt(12)).decode()
        # receive all data from front-end

        if User.list_one(login=username) and User.list_one(email=email):
            # check if login and email already exists in database

            flash("User already exists","error")
            return redirect(url_for("auth.register_user"))
    
        newUser = User(
            login = username,
            fullName = fullName,
            email = email,
            password = password
        ).create()

        #create user and persist your data on database

        if newUser:
            flash("User created successfully","success")
            return redirect(url_for('auth.auth_user'))
            # redirect user case success
        else:
            flash("Failure to create user","error")
            return redirect(url_for('auth.register_user'))
            # redirect user case failure

@auth_routes.route('/logoff', methods=['GET', 'POST'])
def deauth_user():
    if request.method == 'GET':
        
        if current_user.is_authenticated:
        # check if user is authenticated, if positive, logoff them

            logout_user()
            flaskSession.clear()

        return redirect(url_for('auth.auth_user'))
        # Redirect user for login page
    
    if request.method == 'POST':

        if current_user.is_authenticated:
            logout_user()
            flaskSession.clear()
            
            #check same things from GET methods, but in this case, returns TRUE or FALSE about success
            return jsonify({'message':'Success'})
        else:
            return jsonify({'message':'Error'})

from flask import Blueprint, render_template, url_for, request, flash, redirect
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

                login_user(user)

                flash(f"Welcome {user.login}.", "error")
                return redirect(url_for('auth.auth_user'))
            
            flash(f"Invalid credentials.", "error")
            return redirect(url_for('auth.auth_user'))
                

        flash(f"Invalid credentials.", "error")
        return redirect(url_for('auth.auth_user'))

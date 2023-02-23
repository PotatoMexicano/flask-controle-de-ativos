from flask import Blueprint, render_template, url_for, request, flash, redirect

import bcrypt

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Field
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    
    username = StringField('Your username', validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField('Your password', validators=[InputRequired(), Length(min=8, max=64)])
    remember_me = BooleanField('Keep me logged in', default='y')
    submit = SubmitField('Log In')

auth_routes = Blueprint(name='auth', import_name=__name__, template_folder='template', url_prefix='/auth')

@auth_routes.route('/login', methods=['POST'])
def auth_user():
    
    username = request.form.get('username')
    password = bcrypt.hashpw(password=str(request.form.get('password')).encode(), salt=bcrypt.gensalt())
    remember = (True if request.form.get('remember_me') == 'y' else False)

    flash(f"Welcome {username}!", "error")
    return redirect(url_for('auth.view_login'))


@auth_routes.route('/login', methods=['GET'])
def view_login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('login.html')

    data = {'title': 'Login'}
    
    return render_template('login.html', data=data, form=form)


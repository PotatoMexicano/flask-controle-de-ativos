from flask import Blueprint, render_template, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Field
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    
    username = StringField('Your username', validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField('Your password', validators=[InputRequired(), Length(min=8, max=64)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

auth_routes = Blueprint(name='auth', import_name=__name__, template_folder='template', url_prefix='/auth')

@auth_routes.route('/login', methods=['GET','POST'])
def view_login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('login.html')

    data = {'title': 'Login'}
    
    return render_template('login.html', data=data, form=form)


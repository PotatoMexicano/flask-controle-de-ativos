from flask import Blueprint, request, render_template
from flask_login import current_user, login_required
from app import app, db
home_routes = Blueprint(name='homepage', import_name=__name__, template_folder='template', url_prefix='')

@home_routes.route('/', methods=['GET'])
@login_required
def homepage():
    if request.method == 'GET':

        user_fullName_splited = str(current_user.fullName).split(' ')
        firstName = user_fullName_splited[0][0]
        lastName = user_fullName_splited[-1][0]

        return render_template('homepage.html', data={
            'title':'Homepage',
            'logo_alt': app.config['COMPANY_NAME'],
            'company_name': app.config['COMPANY_NAME'],
            'userLogoBuilder': str(firstName)+str(lastName)
        })

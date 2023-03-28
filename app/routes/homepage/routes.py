from flask import Blueprint, request, render_template
from flask_login import current_user, login_required
from app.models.Model import LogisticCenter
from app import app, db

home_routes = Blueprint(name='homepage', import_name=__name__, template_folder='../templates', url_prefix='')

@home_routes.route('/', methods=['GET'])
@login_required
def homepage():
    if request.method == 'GET':

        firstName, lastName = current_user.split()

        return render_template('./home/homepage.html', data={
            'title':'Homepage',
            'logo_alt': app.config['COMPANY_NAME'],
            'company_name': 'Company',
            'userLogoBuilder': str(firstName)+str(lastName),
            'dataTable': LogisticCenter.list_all(tags=True),
        })

from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict
from app.models import Product
from app import app, db

product_routes = Blueprint(name='product', import_name=__name__, template_folder='../templates', url_prefix='/product')

def load_data():
    firstName, lastName = current_user.split()

    data = {'title':'Product',
        'logo_alt': app.config['COMPANY_NAME'],
        'company_name': 'Company',
        'userLogoBuilder': str(firstName)+str(lastName)
    }
    return data

@product_routes.route('/', methods=['GET'])
@login_required
def render_table_product():   
    return render_template('product/homepage.html', data = load_data())

@product_routes.route('/list-all', methods=['GET','POST'])
@login_required
def list_all_product():

    if request.method == 'POST':

        all_product = Product.list_all()

        return jsonify(all_product)

    if request.method == 'GET':

        all_product = Product.list_all()

        return jsonify(all_product)

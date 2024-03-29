from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict
from app.models import LogisticCenter
from app import app, db

logistic_routes = Blueprint(name='logistic', import_name=__name__, template_folder='./templates', url_prefix='/logistic')

def load_data():
    firstName, lastName = current_user.split()

    data = {'title':'Logistic Center',
        'logo_alt': app.config['COMPANY_NAME'],
        'company_name': 'Company',
        'userLogoBuilder': str(firstName)+str(lastName)
    }
    return data

@logistic_routes.route('/', methods=['GET'])
@login_required
def render_table_logistic_center():   

    return render_template('homepage_logistic_center.html', data = load_data())

@logistic_routes.route('/add', methods=['POST'])
@login_required
def add_logistic_center():
    if request.method == 'POST':
        
        response = LogisticCenter(
            name = request.form.get('name'),
            zipcode = request.form.get('zipcode'),
            address = request.form.get('address'),
            district = request.form.get('district'),
            city = request.form.get('city'),
            state = request.form.get('state'),
            country = request.form.get('country'),
            phoneOne = request.form.get('phone_one'),
            phoneTwo = request.form.get('phone_two'),
            email = request.form.get('email')
        ).create()


        if bool(response['status']):
            return jsonify(response), 201

        return jsonify(response), 404

@logistic_routes.route('/edit/<id>', methods=['GET','POST'])
@login_required
def edit_logistic_center(id: int):

    if request.method == 'POST':

        if not id:
            flash(f"Error when call endpoint","error")
            return jsonify('route require [id] for edit.')

        logistic = LogisticCenter.list_one(id = id)

        if not logistic:
            flash(f"Logistic center not found","error")
            return jsonify(None)

        request_original = request.form
        
        checked = request.form.get('checked')
        
        checked = True if checked == 'true' else False

        request_with_enabled = ImmutableMultiDict(list(request_original.items()) + [('enabled', bool(checked))])

        logistic.update(request_with_enabled)

        flash(f"Logistic center updated !","success")
        return redirect(url_for('logistic.render_table_logistic_center'))

@logistic_routes.route('/list-one/<id>', methods=['GET','POST'])
@login_required
def list_one_logistic_center(id: int):
        
    one_logistic_center = LogisticCenter.list_one(id=id)
        
    return jsonify(one_logistic_center)

@logistic_routes.route('/list-all', methods=['GET','POST'])
@login_required
def list_all_logistic_center():

    if request.method == 'POST':

        all_logistic_center = LogisticCenter.list_all()

        return jsonify(all_logistic_center)

    if request.method == 'GET':

        all_logistic_center = LogisticCenter.list_all()

        return jsonify(all_logistic_center)

@logistic_routes.route('/download/list-all', methods=['POST'])
@login_required
def download_list_all_logistic_center():
        if request.method == 'POST':
            all_logistic_center = LogisticCenter.list_all()

            response = jsonify(all_logistic_center).get_json()

            return jsonify(response)

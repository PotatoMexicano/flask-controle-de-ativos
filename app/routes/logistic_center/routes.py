from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user, login_required
from app.models.Model import LogisticCenter
from app import app, db

logistic_routes = Blueprint(name='logistic-center', import_name=__name__, template_folder='template', url_prefix='/logistic')

@logistic_routes.route('/list-all-countries', methods=['POST'])
def list_all_countries():
    from restcountries import RestCountryApiV2 as rapi
    return jsonify([a.name for a in rapi.get_all()])
     

@logistic_routes.route('/list-all', methods=['GET','POST'])
@login_required
def list_all_logistic_center():

    if request.method == 'POST':

        loadTags = bool(request.form.get('tags'))

        all_logistic_center = LogisticCenter.list_all(tags=loadTags)

        return jsonify(all_logistic_center)

    if request.method == 'GET':

        all_logistic_center = LogisticCenter.list_all(tags=True)

        return jsonify(all_logistic_center)

@logistic_routes.route('/download/list-all', methods=['POST'])
@login_required
def download_list_all_logistic_center():
        if request.method == 'POST':
            all_logistic_center = LogisticCenter.list_all(tags=True)

            response = jsonify(all_logistic_center).get_json()

            for index, data in enumerate(response):
                data['tags'] = ', '.join(str(x) for x in [tag['name'] for tag in data['tags']])

            return jsonify(response)



from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user, login_required
from app.models.Model import LogisticCenter
from app import app, db

logistic_routes = Blueprint(name='logistic-center', import_name=__name__, template_folder='template', url_prefix='/logistic')

@logistic_routes.route('/list-all', methods=['GET'])
@login_required
def list_all_logistic_center():
    if request.method == 'GET':

        all_logistic_center = LogisticCenter.list_all(tags=False)

        return jsonify(all_logistic_center)

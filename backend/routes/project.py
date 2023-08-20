from flask import Blueprint, request, jsonify

from services.User_tokens import User_tokens
from models.Files import Files

project = Blueprint('project', __name__)

@project.route('/get-seq/<string:ci_project>')
def get_seq(ci_project):
    token_consult = User_tokens.verify_token(request.headers)
    if token_consult:
        consulta = Files.get_sequences(ci_project)
        return jsonify(consulta)
    else:
        response = jsonify(message="No autorizado")
        return response, 401
from flask import Blueprint, request, jsonify

from services.User_tokens import User_tokens
from models.Projects import Projects

main = Blueprint("new_project", __name__)


@main.route("/", methods=["POST"])
def new_project():
    if request.method == "POST":
        token_consult = User_tokens.verify_token(request.headers)
        if token_consult:
            try:
                project_name = request.form["project_name"]
                add_project = Projects.create_project (token_consult, project_name)
                if add_project:
                    print("Creando las tablas relacionadas con el proyecto")
                    if Projects.create_project_tables(add_project): 
                        return jsonify(message="Proyecto creado correctamente.", success=True)
                    else:
                        return jsonify (message="Error en la creación de las tablas.", success=False)
                else:
                    return jsonify (message="Error en la creación del proyecto.", success=False)
            except:
                response = jsonify(message="Algo salió mal en la creación del proyecto.")
                return response, 401
            
        else:
            response = jsonify(message="No autorizado")
            return response, 401

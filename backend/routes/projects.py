from flask import Blueprint, request, jsonify

from services.User_tokens import User_tokens
from models.Projects import Projects

prjt = Blueprint('prjt', __name__)


@prjt.route('/new-project/<int:user_id>', methods=["POST"])
def new_project(user_id):
    if request.method == "POST":

        # la consulta al token devuelve el id del usuario que crea el proyecto
        token_consult = User_tokens.verify_token(request.headers)

        if token_consult:
            try:
                # Guarda el la tabla 'projects' el nombre del proyecto con el propietario.
                project_name = request.form["project_name"]
                if token_consult == user_id:
                    add_project = Projects.create_project (token_consult, project_name)
                else:
                    add_project = False
                # Si el proyecto se guardó crea las tablas en la base de datos necesarias
                # para el proyecto: _cast -> Reparto de personajes que pertenecen al proyeco.
                #                   _seq_cast -> Reparto de personajes por secuencia.
                #                   _sequences -> Descripción de cada secuencia.
                #                   _guiones -> Los guiones que pertenecen al proyecto.
                if add_project:
                    print("Creando las tablas relacionadas con el proyecto")
                    if Projects.create_project_tables(add_project): 
                        return jsonify(message="Proyecto creado correctamente.", success=True)
                    else:
                        return jsonify (message="Error en la creación de las tablas.", success=False)
                else:
                    return jsonify (message="Error al guardar el proyecto.", success=False)
            except:
                response = jsonify(message="Algo salió mal en la creación del proyecto.")
                return response, 401
            
        else:
            response = jsonify(message="No autorizado")
            return response, 401

@prjt.route('/list-project')
def get_project():
    token_consult = User_tokens.verify_token(request.headers)
    if token_consult:
        consulta = Projects.get_projects(token_consult)
        return jsonify(consulta)
    else:
        response = jsonify(message="No autorizado")
        return response, 401

@prjt.route('/delete/<string:ci_project>', methods=['DELETE'])
def del_project(ci_project):
    token_consult = User_tokens.verify_token(request.headers)
    if token_consult and request.method == 'DELETE':
        consulta = Projects.delete_project(ci_project, token_consult)
        return jsonify(consulta)
    else:
        response = jsonify(message="No autorizado")
        return response, 401
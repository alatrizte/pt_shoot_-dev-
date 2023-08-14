from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os, time

from services.create_xml import create_xml, xml_to_db_guion
from services.User_tokens import User_tokens
from models.Files import Files

main = Blueprint('upload', __name__)

@main.route("/", methods=['POST'])
def uploader():
    # primero autorizamos si el usuario está registrado.
    token_consult = User_tokens.verify_token(request.headers)
    
    if token_consult:
        cwd = os.getcwd()  # Get the current working directory (cwd)
        if request.method == "POST":
            ciProject = request.form['ciProject']
            UPLOAD_FOLDER = cwd + '/backend/uploads/' + ciProject
            # ALLOWED_EXTENSIONS = {'doc'}
        
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
                os.chmod(UPLOAD_FOLDER, 0o777)

            # obtenemos el archivo del input "archivo"
            file = request.files["archivo"]
            filename = secure_filename(file.filename)

            # Guardamos el archivo en el directorio "uploads"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            # subprocess.call(['soffice', '--headless', '--convert-to', 'html:XHTML Writer File:UTF8', file_doc])
            
            #ruta = f"backend/uploads/{ciProject}/"
            file_doc = f"{UPLOAD_FOLDER}/{filename}"
            nombre_archivo = os.path.splitext(os.path.basename(file_doc))[0]
            fileHTML = "backend/uploads/" + ciProject + "/" + nombre_archivo + ".html"
            
            # Convierte el archivo .doc en un .html
            os.system (f"soffice --headless --convert-to 'html:XHTML Writer File:UTF8' {file_doc} --outdir {UPLOAD_FOLDER}")

            # Espera a que el archivo .html esté creado
            while not os.path.exists(fileHTML):
                time.sleep(1)
            
            # Convierte el archivo .html en un .xml con los datos limpios.
            file_xml = create_xml(ciProject, nombre_archivo)
            print("El archivo " + nombre_archivo + ".xml se ha creado.")

            # Extrae los datos del XML de descripción del guión para guardarlo en la tabla [ci_project]_guiones
            # devuelve una lista.[id, titulo, capitulo, dialogos, argumento, edicion, vers, name_xml]
            data_guiones = xml_to_db_guion(file_xml) 
            registro_db = Files.guiones(data_guiones, ciProject)

            # Retornamos una respuesta satisfactoria
            return jsonify(registro_db)
    
    else:
        response = jsonify(message="No autorizado")
        return response, 401
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os, time

from services.create_xml import create_xml
from services.User_tokens import User_tokens

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

            os.system (f"soffice --headless --convert-to 'html:XHTML Writer File:UTF8' {file_doc} --outdir {UPLOAD_FOLDER}")

            while not os.path.exists(fileHTML):
                time.sleep(1)
            
            create_xml(ciProject, nombre_archivo)
            print("El archivo " + nombre_archivo + ".xml se ha creado.")
            
            # Retornamos una respuesta satisfactoria
            return jsonify(message="Archivo subido con éxito", success=True)
    
    else:
        response = jsonify(message="No autorizado")
        return response, 401
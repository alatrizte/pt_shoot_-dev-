from flask import Blueprint, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os, time

from services.create_xml import create_xml

main = Blueprint('upload', __name__)

@main.route("/", methods=['POST'])
def uploader():

    load_dotenv()
    user_pass = os.getenv("PASS_ROOT")
    cwd = os.getcwd()  # Get the current working directory (cwd)

    if request.method == "POST":
        ciProject = request.form['ciProject']
        UPLOAD_FOLDER = cwd + '/backend/uploads/' + ciProject
        # ALLOWED_EXTENSIONS = {'doc'}
        # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            os.chmod(UPLOAD_FOLDER, 0o777)

        # obtenemos el archivo del input "archivo"
        file = request.files["archivo"]
        filename = secure_filename(file.filename)
        # Guardamos el archivo en el directorio "uploads"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        os.system(f"echo {user_pass} | sudo -S unoconv -f xhtml backend/uploads/{ciProject}/{filename}")

        ruta = "backend/uploads/" + ciProject + "/" + filename
        nombre_archivo = os.path.splitext(os.path.basename(ruta))[0]
        fileHTML = "backend/uploads/" + ciProject + "/" + nombre_archivo + ".html"

        while not os.path.exists(fileHTML):
            time.sleep(1)
        
        create_xml(ciProject, nombre_archivo)
        print("El archivo " + nombre_archivo + ".xml se ha creado.")
        
        # Retornamos una respuesta satisfactoria
        return {'upload': 'ok'}
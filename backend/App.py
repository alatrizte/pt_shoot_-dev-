from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import time
import hashlib

from backend.services.create_xml import create_xml
from backend.models.users import userLogin

app = Flask(__name__)

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha3_256((request.form['password'].encode('utf-8'))).hexdigest()

        consulta = userLogin(email, password)
        if consulta == "no data":
            return jsonify ( message=consulta, success=False)
        else:
            return jsonify( id=consulta[0],
                            username=consulta[1],
                            message='success',
                            success=True
                            )

@app.route("/upload", methods=['POST'])
def uploader():
    cwd = os.getcwd()  # Get the current working directory (cwd)

    if request.method == "POST":
        ciProject = request.form['ciProject']
        UPLOAD_FOLDER = cwd + '/backend/uploads/' + ciProject
        ALLOWED_EXTENSIONS = {'doc'}
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # obtenemos el archivo del input "archivo"
        file = request.files["archivo"]
        filename = secure_filename(file.filename)
        # Guardamos el archivo en el directorio "uploads"
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        
        os.system("sudo unoconv -f xhtml backend/uploads/" + ciProject + "/" + filename)

        ruta = "backend/uploads/" + ciProject + "/" + filename
        nombre_archivo = os.path.splitext(os.path.basename(ruta))[0]
        fileHTML = "backend/uploads/" + ciProject + "/" + nombre_archivo + ".html"

        while not os.path.exists(fileHTML):
            time.sleep(1)
        
        create_xml(ciProject, nombre_archivo)
        print("El archivo " + nombre_archivo + ".xml se ha creado.")
        
        # Retornamos una respuesta satisfactoria
        return {'upload': 'ok'}

if __name__ == "__main__":
    # Iniciamos la aplicación
    app.run(debug=True)

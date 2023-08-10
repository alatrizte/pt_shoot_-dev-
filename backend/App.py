from flask import Flask
from routes import login
from routes import upload

app = Flask(__name__)

app.register_blueprint(login.main, url_prefix='/login')
app.register_blueprint(upload.main, url_prefix='/upload')

if __name__ == "__main__":
    # Iniciamos la aplicación
    app.run(debug=True)

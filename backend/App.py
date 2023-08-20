from flask import Flask
from routes import login
from routes import upload
from routes import projects
from routes import project

app = Flask(__name__)

app.register_blueprint(login.auth)
app.register_blueprint(upload.main, url_prefix='/upload')
app.register_blueprint(projects.projects)
app.register_blueprint(project.project)

if __name__ == "__main__":
    # Iniciamos la aplicación
    app.run(debug=True)

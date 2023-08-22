from flask import Blueprint, request, jsonify

from models.Users import Users
from services.User_tokens import User_tokens
import hashlib

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        #password = hashlib.sha3_256((request.form['password'].encode('utf-8'))).hexdigest()

        password = request.form['password']

        consulta = Users.login(email, password)
        if consulta['success'] == False:
            return jsonify ( message=consulta['message'], success=False)
        else:
            encoded_token = User_tokens.generate_token(consulta['message'])
            return jsonify( message='success',
                            success=True,
                            token=encoded_token
                            )
        
@auth.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['user_name']
        email = request.form['user_mail']
        
        # Comprueba el servidor que el password y la confirmación sean iguales.
        # En caso afirmativo hashea la contraseña con 'sha3-256'
        if request.form['password'] == request.form['pass_confirm']:
            password = hashlib.sha3_256((request.form['password'].encode('utf-8'))).hexdigest()
        
        consulta = Users.signup(name, email, password)
        if consulta['success'] == False:
            return jsonify(message=consulta['message'], success=False)
        else:
            return jsonify(message=consulta['message'], success=True)
        
@auth.route('/mail_confirm', methods=['POST'])
def confirm():
    if request.method == 'POST':
        email = request.form['email']
        key = request.form['key']

        consulta = Users.mail_confirm(email, key)
        if consulta['success'] == True:
            return jsonify(message=consulta['message'], success=True)
        else:
            return jsonify(message=consulta['message'], success=False)
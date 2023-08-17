from flask import Blueprint, request, jsonify

from models.Users import Users
from services.User_tokens import User_tokens
import hashlib

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha3_256((request.form['password'].encode('utf-8'))).hexdigest()

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
        name = request.form['name']
        email = request.form['email']
        password = hashlib.sha3_256((request.form['password'].encode('utf-8'))).hexdigest()

        consulta = Users.signup(name, email, password)
        if consulta['success'] == False:
            return jsonify(message= consulta['message'])
        else:
            return jsonify(message=consulta['message'])
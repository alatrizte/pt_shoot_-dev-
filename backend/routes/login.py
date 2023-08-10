from flask import Blueprint, request, jsonify

from models.users import userLogin
from services.User_tokens import User_tokens
import hashlib

main = Blueprint('login', __name__)

@main.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hashlib.sha3_256((request.form['password'].encode('utf-8'))).hexdigest()

        consulta = userLogin(email, password)
        if consulta == "no data":
            return jsonify ( message=consulta, success=False)
        else:
            encoded_token = User_tokens.generate_token(consulta)
            return jsonify( message='success',
                            success=True,
                            token=encoded_token
                            )
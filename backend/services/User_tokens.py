import datetime
import pytz
import jwt
from dotenv import load_dotenv
import os

class User_tokens():

    load_dotenv()
    secret = os.getenv("JWT_KEY")
    time_zn = pytz.timezone("Europe/Madrid")

    @classmethod
    def generate_token(cls, user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.time_zn),
            'exp': datetime.datetime.now(tz=cls.time_zn)+ datetime.timedelta(minutes=10),
            'username': user[1],
            'id': user[0],
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")
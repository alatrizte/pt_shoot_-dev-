import datetime
import pytz
import jwt
from dotenv import load_dotenv
import os


class User_tokens:
    load_dotenv()
    secret = os.getenv("JWT_KEY")
    time_zn = pytz.timezone("Europe/Madrid")

    @classmethod
    def generate_token(cls, user):
        now = datetime.datetime.now(tz=cls.time_zn)
        payload = {
            "iat": now,
            "exp": now + datetime.timedelta(minutes=10),
            "username": user[1],
            "id": user[0],
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if "Authorization" in headers.keys():
            authorization = headers["Authorization"]
            encoded_token = authorization.split(" ")[1]

            try:
                payload = jwt.decode(
                    encoded_token, cls.secret, algorithms=["HS256"]
                )
                return payload['id']
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False

        return False

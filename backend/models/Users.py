from database import db
import string, random
from services.send_mail_key import send_

class Users:

    @classmethod
    def login(cls, email, password):

        print(email, password)
        sql = "SELECT * FROM users WHERE user_mail=%s AND user_pass=%s AND key_confirm=%s"
        values=(email, password, 'confirm!')
        conn = db.query(sql, values)

        if len(conn) > 0:
            return {"message": conn[0], "success": True}
        else: 
            return {"message": "Ha de estar registrado para poder acceder.", "success": False}

    @classmethod  
    def signup(cls, name, email, password):
        # Comprueba que el email sea único.
        sql = f"SELECT * FROM users WHERE user_mail=%s"
        val = (email,)

        is_unique_mail = db.query(sql, val)

        if len(is_unique_mail) > 0:
            return {"message": "El e-mail ya está registrado", "success": False}
        else:
            # Genera una key aleatoria para el nuevo usuario
            # Esta llave se envia por mail para confirmar su registro.
            key = ''
            for x in range(8):
                key += random.choice(string.ascii_letters + string.digits)

            sql = f"INSERT INTO users (user_name, user_mail, user_pass, key_confirm) VALUES (%s, %s, %s, %s)"
            val = (name, email, password, key)

            conn = db.insert(sql, val)

            if conn:
                send_(email, key)
            return {"message": "Consulte su e-mail para terminar el registro.", "success": True}
        
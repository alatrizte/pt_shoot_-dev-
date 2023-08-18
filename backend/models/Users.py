from database import db
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

        # Si el e-mail no es único devuelve error
        if len(is_unique_mail) > 0:
            return {"message": "El e-mail ya está registrado", "success": False}
        else:  
            # Inserta en la tabla 'users' los datos del usuario.      
            sql = f"INSERT INTO users (user_name, user_mail, user_pass) VALUES (%s, %s, %s)"
            val = (name, email, password)
            conn = db.insert(sql, val)

            # Si la respuesta de la base de datos es correcta
            # Enviamos un correo con una clave. Es la función send_ la encargada de generar la clave
            # Si todo es correcto la función nos devuelve la clave que envió por correo.
            # La clave la almacena en la base de datos en la tabla 'users'.
            if conn:
                consulta = cls.send_key(email, name)
                return consulta

    @classmethod
    def send_key(cls, email, name):
        key_sended = send_(email, name)
        sql = f"UPDATE users SET key_confirm=%s WHERE user_mail=%s"
        val = (key_sended['key'], email)
        conn = db.insert(sql, val)

        return {"message": "Consulte su e-mail para terminar el registro.", "success": True}
    
    @classmethod
    def mail_confirm(cls, mail, key):
        sql = f"SELECT * FROM users WHERE user_mail=%s AND key_confirm=%s"
        val = (mail, key)

        confirm = db.query(sql, val)

        if len(confirm) > 0:
            sql = f"UPDATE users SET key_confirm='confirm!' WHERE user_mail=%s"
            val = (mail,)
            
            conn = db.insert(sql, val)

            return {"message": "Usuario registrado correctamente.", "success": True}
        
        return {"message": "El código o el e-mail no son correctos", "success": False}
        
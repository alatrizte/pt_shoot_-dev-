from database import db

class Users:

    @classmethod
    def login(cls, email, password):

        print(email, password)
        sql = "SELECT * FROM users WHERE user_mail=%s AND user_pass=%s"
        values=(email, password)
        conn = db.query(sql, values)

        if len(conn) > 0:
            return {"message": conn[0], "success": True}
        else: 
            return {"message": "Sin datos de logeo", "success": False}
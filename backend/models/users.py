from database import db

def userLogin(email, password):

    print(email, password)
    sql = "SELECT * FROM users WHERE user_mail=%s AND user_pass=%s"
    values=(email, password)
    conn = db.query(sql, values)

    if len(conn) > 0:
        return conn[0]
    else: 
        return "no data"
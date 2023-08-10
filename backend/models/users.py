from database.db import query

def userLogin(email, password):

    print(email, password)
    sql = f"SELECT * FROM users WHERE user_mail='{email}' AND user_pass='{password}'"
    conn = query(sql)

    if len(conn) > 0:
        return conn[0]
    else: 
        return "no data"
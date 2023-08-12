from database import db
import zlib, datetime

class Projects:
    
    @classmethod
    def create_project(cls, user_id, name_project):

        now = datetime.datetime.now()
        # Concatena el nombre del proyecto y now para extraer un codigo de projecto
        data = f'{name_project} {now}' 
        ci_project = format(zlib.adler32(data.encode()), '08x')

        sql = "INSERT INTO projects(user_id, ci_project, name_project) VALUES (%s, %s, %s)"
        val = (user_id, ci_project, name_project,)
        try:
            consulta = db.insert(sql, val)
            print(consulta)
            return True
        except:
            return False
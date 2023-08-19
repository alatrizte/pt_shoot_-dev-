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
            db.insert(sql, val)
            return ci_project
        except:
            return False
        
    @classmethod
    def create_project_tables(cls, ci_project):
        inserts = []
        # Al crear un nuevo proyecto se generan las tablas relacionadas con ese proyecto.
        # tabla de guiones
        tablename = f"{ci_project}_guiones"
        sql_guiones = f"CREATE TABLE IF NOT EXISTS {tablename} ( \
                id VARCHAR(8) PRIMARY KEY, \
                titulo VARCHAR(255) NOT NULL UNIQUE,\
                capitulo INT, \
                dialogos VARCHAR(50),\
                argumento VARCHAR(50),\
                edicion VARCHAR(50),\
                vers VARCHAR (10),\
                name_xml VARCHAR (255))"
        inserts.append((sql_guiones,""))
      
        # tabla de persojajes en el proyecto
        tablename = f"{ci_project}_cast"
        sql_cast = f"CREATE TABLE IF NOT EXISTS {tablename} (\
                id VARCHAR(8) PRIMARY KEY,\
                nc INT UNIQUE,\
                character_name VARCHAR(50) NOT NULL UNIQUE,\
                actor_name VARCHAR(100))"
        inserts.append((sql_cast,""))

        # tabla de secuencias
        tablename = f"{ci_project}_sequences"
        sql_sequences = f"CREATE TABLE IF NOT EXISTS {tablename}( \
                id VARCHAR(8) PRIMARY KEY NOT NULL,\
                ord INT NOT NULL,\
                cap INT NOT NULL,\
                sec VARCHAR (8) NOT NULL,\
                localizacion VARCHAR(64) NOT NULL,\
                ubicacion VARCHAR (16),\
                ambiente VARCHAR (16),\
                duracion INT,\
                plan VARCHAR (16),\
                doit BOOLEAN)"
        inserts.append((sql_sequences,""))
  

        # tabla de personajes por secuencia
        tablename = f"{ci_project}_seq_cast"
        sql_seq_cast = f"CREATE TABLE IF NOT EXISTS {tablename} (\
                id VARCHAR(8) NOT NULL,\
                cast VARCHAR (8) NOT NULL,\
                PRIMARY KEY (id, cast),\
                off_dialog INT )"
        inserts.append((sql_seq_cast,""))
        
        print ("envio a transacciones")
        crea_tablas = db.transactions(inserts)
        print (crea_tablas)
        return crea_tablas

    @classmethod
    def get_projects(cls, user):
        sql = f"SELECT * FROM projects WHERE user_id=%s"
        val = (user, )

        consulta = db.query(sql, val)

        if len(consulta) > 0:
            return consulta
        else:
            return {"message": "Todavía este Usuario no tiene proyectos", "success": False}
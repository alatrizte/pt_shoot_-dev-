from database import db

class Files:

    @classmethod
    def guiones(cls, data, ci_project):
        sql = f"REPLACE INTO {ci_project}_guiones VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data)
        print(f"insertando datos en {ci_project}_guiones")
        try:
            if db.insert(sql, val):
                return {"message": "Guión registrado exitosamente", "success": True}
            
        except Exception as e:
            return {"message": e, "success": False}

    @classmethod  
    def sequences(cls, data, ci_project):
        sql = f"REPLACE INTO {ci_project}_sequences VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data)
        try:
            if db.insert(sql, val):
                return {"message": "Añadido satisfactoriamente", "success": True}
        except Exception as e:
            return {"message": f"Error al introducir al sec id {data[0]}: {e}", "success": False}
        
    @classmethod
    def casting(cls, data, ci_project):  
        # key = nombre personaje
        # value = id      
        for key, value in data.items():
            # Consulta para saber el último numero de personaje 'nc'
            sql = f"SELECT nc FROM {ci_project}_cast order by nc DESC LIMIT 1"
            consulta = db.query(sql, '')

            # Caso afirmativo sumamos 1 a 'nc'
            if consulta:
                nc = consulta[0][0] + 1
            else:
                nc = 1 # Caso de ser el primer personaje en el proyecto.

            # Consulta sql para introducir el nombre del personaje
            sql = f"INSERT IGNORE INTO {ci_project}_cast (id, nc, character_name) VALUES (%s, %s, %s)"
            val = (value, nc, key)
            try:
                db.insert(sql, val) # Envío a la Base de Datos.
            except Exception as e:
                error = f"Error al introducir el personaje {key}: {e}" 
                return {"message": error, "success": False}
            
        return {"message": "Lista de personajes añadidos a la base de datos", "success": True}
    
    @classmethod
    def cast_seq(cls, data, ci_project):

        # Buscamos en la tabla _cast el id del personaje.
        sql = f"SELECT id FROM {ci_project}_cast WHERE character_name=%s"
        val = (data[1],)
        id_nombre = db.query(sql, val)

        # Si devuelve un id el personaje tiene dialogo y lo almacenamos en la tabla _seq_cast.
        try:
           sql = f"INSERT IGNORE INTO {ci_project}_seq_cast (id, cast, off_dialog) VALUES (%s, %s, %s)"
           val = (data[0], id_nombre[0][0], data[2])
           db.insert(sql, val)
        except:
            pass
        
        return {"message": f"Datos introducidos correctamente en la tabla {ci_project}_seq_cast", "success": True}
    
    @classmethod
    def get_sequences(cls, ci_project):
        sql = f"SELECT * FROM {ci_project}_sequences"
        try:
            consulta = db.query(sql, '')
            return consulta
        except Exception as e:
            return {"message": f"Error de consulta en la tabla {ci_project}_sequences: {e}", "success": False}
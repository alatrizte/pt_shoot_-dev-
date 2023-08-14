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

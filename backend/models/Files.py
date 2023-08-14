from database import db

class Files:

    @classmethod
    def guiones(cls, data, ci_project):
        sql = f"INSERT INTO {ci_project}_guiones(id, titulo, capitulo, dialogos, argumento, edicion, vers, name_xml) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        print(f"insertando datos en {ci_project}_guiones")
        try:
            if db.insert(sql, val):
                return {"message": "Guión registrado exitosamente", "success": True}
            
        except Exception as e:
            return {"message": e, "success": False}
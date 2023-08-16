from bs4 import BeautifulSoup
from models.Files import Files
import re, zlib, os, math

# Función para convertir los archivos html a un archivo con etiquetas xml.
def create_xml(ciProject, fileName):
    path = f"./backend/uploads/{ciProject}/" 
    fileHTML =  path + fileName + ".html"

    # Leer el archivo HTML
    with open(fileHTML, "r") as archivo:
        contenido = archivo.read()

    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(contenido, "html.parser")

    # Selecciona los estilos dentro de la etiqueta <style>
    styles = soup.find_all("style") 

    # Cada linea es una definición de estilos.
    tags = styles[0].string.split('\n')

    # Crea un diccionario para almacenar los estilos.
    rules = {}

    for tag in tags:

        cadena = tag.strip()

        # Selecciona lo que está entre llaves para obtener valores del diccionario.
        patron = r"\{(.+?)\}"
        valor = re.search(patron, cadena)
        if valor:
            valor = valor.group(1)    
            valor = valor.split(";")

        # Selecciona lo que no está entre llaves para obtener la llave del diccionario.
        patron = r"(.*?)\{.*?\}"
        key = re.search(patron, cadena)
        if key:
            key = key.group(1).strip()
            rules.update({key:valor}) # Se añade al diccionario.

    # ------------- LISTAS CON ESTILOS -----------------

    # Crea una lista para los estilos del título del guion.
    tit_cls = []
    for k, v in rules.items():
        if ' font-size:50pt' in v:
            tit_cls.append(k.replace(".", ""))

    # Crea una lista con los estilos que definen el titulo del episodio.
    episodio_cls = []
    for k, v in rules.items():
        if ' font-size:24pt' in v:
            episodio_cls.append(k.replace(".", ""))

    # Crea una lista para los estilos de los créditos.
    creditos_cls = []
    for k, v in rules.items():
        if ' font-size:14pt' in v:
            creditos_cls.append(k.replace(".", ""))

    # Crea una lista de setilos donde coincida con los parámetros de una secuencia.
    sec_cls = []
    for k, v in rules.items():
        if ' font-size:12pt' in v  and ' font-weight:bold' in v: 
            sec_cls.append(k.replace(".", ""))

    # Crea una lista de estilos donde coincidan los parámetros de personajes de secuencia.
    nomes_cls = []
    for k,v in rules.items():
        if ' font-style:italic' in v and ' margin-left:0.63cm' in v:
            nomes_cls.append(k.replace(".", ""))

    # Crea una lista para los estilos que tengan la propiedad { font-style:italic }.
    italics_cls = []
    for k, v in rules.items():
        if ' font-style:italic' in v:
            italics_cls.append(k.replace(".", ""))

    # Crea una lista para los estilos de las acotaciones
    # esta lista se crea extrayendo de la lista de italics_cls las que están en nomes_cls
    acot_cls = list(set(italics_cls) - set(nomes_cls))

    # Crea una lista con los estilos que tengan un { margin-left:3.501cm;}
    marginlf_cls = []
    for k, v in rules.items():
        if ' margin-left:3.501cm' in v:
            marginlf_cls.append(k.replace(".", ""))

    # Crea una lista de los estilos con los diálogos
    # obteniendola de la diferencia entre la lista de marginlf_cls y acot_cls.
    dlg_cls = list(set(marginlf_cls) - set(acot_cls))

    # -----------------------------------------------------------

    # Crea un archivo XML

    fileXML = open (path + fileName + ".xml", "w")
    fileXML.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    fileXML.write('<capitulo>\n')

    # Acceder a elementos HTML
    parrafos = soup.find_all("p")

    # variable para indicar cuando empieza una <part> que es el bloque de secuencia.
    open_sec = True

    for parrafo in parrafos:
        # busca la clase de titulo
        if parrafo['class'][0] in tit_cls:
            fileXML.write("<titulo>" + parrafo.text + "</titulo>\n")

        # busca las clases de episodio
        if parrafo['class'][0] in episodio_cls:
            fileXML.write("<episodio>" + parrafo.text + "</episodio>\n")

        # busca las clases de creditos
        if parrafo['class'][0] in creditos_cls and (parrafo.text).strip() != "":
            fileXML.write("<creditos>" + parrafo.text + "</creditos>\n")

        # busca las clases de las secuencias
        if parrafo['class'][0] in sec_cls and (parrafo.text).strip() != "":

            # si la bandera es false es que no es inicio de una secuencia y por ello cierra la etiqueta <part>
            if open_sec == False:
                fileXML.write("</part>\n")

            sec = parrafo.text.upper()
            tiene_intercut = ""
            if 'INTERCUT' in sec:
                sec = sec.replace("-INTERCUT-", "")
                tiene_intercut = 'intercut="true"'
            # crea una lista de los datos de la secuencia CAPITULO, NUMERO SEC, LOCALIZACION, UBICACION, AMBIENTE
            seclist = sec.split(".")
            # Si la lista tiene parametros
            if len(seclist) > 2:
                cap = seclist[0]    # CAPITULO
                num = seclist[1]    # NUMERO SEC
                ub = ""             # UBICACION
                ub_flag = True      # bandera que indica que los datos de ubicación ya aparecieron
                loc = ""            # LOCALIZACIÓN
                amb = ""            # AMBIENTE

                # inicia el bloque de secuencia
                fileXML.write("<part id = '" + num + "'>\n")
                
                for item in seclist:    
                    if 'EXT' in item or 'INT' in item or 'NAT' in item:
                        
                        ub += item
                        ub_flag = False # cambia la bandera a false para indicar que lo siguiente es ambiente

                    elif ub_flag and seclist.index(item) > 1:
                        # con la bandera en true estos datos son de localización.
                        loc += item + "."

                    elif seclist.index(item) > 2:
                        amb += item
                        
                fileXML.write(f"<sec {tiene_intercut}><cap>"+cap+"</cap><num>"+num+"</num><loc>"+loc.strip()+"</loc><ub>"+ub.strip()+"</ub><amb>"+amb.strip()+"</amb></sec>\n")
            else: # si la lista no tiene parametros
                fileXML.write("<part>\n")
                fileXML.write("<sec>" + sec + "</sec>\n")
            
            # cerramos la bandera de bloque de secuencia
            open_sec = False

        # busca las clases de las acotaciones
        if parrafo['class'][0] in acot_cls and (parrafo.text).strip() != "":
            # cuenta el número de caracteres de las acotaciones
            size = str(len(parrafo.text))
            fileXML.write("<acot size = '" + size + "'>" + parrafo.text + "</acot>\n")

        # busca las clases de los nombres de los personajes
        if parrafo['class'][0] in nomes_cls and (parrafo.text).strip() != "":
            fileXML.write("<perx>" + parrafo.text.upper() + "</perx>\n")

        # busca las clases de los dialogos
        if parrafo['class'][0] in dlg_cls and (parrafo.text).strip() != "":
            dlg = parrafo.text
            # extrae la primera palabra del dialogo que coincide con el nombre del personaje
            personaje = dlg.split()[0] 
            # elimina del texto el nombre
            texto = dlg.replace(personaje, "")
            # cuenta el número de caracteres del texto
            size = str(len(texto))
            fileXML.write("<dlg size = '" + size + "'><per>" + personaje + "</per>" + texto.strip() + "</dlg>\n")

    fileXML.write('</part>\n')
    fileXML.write('</capitulo>\n')
    fileXML.close()
    return (path + fileName + ".xml")

# Función para añadir a la tabla [ci_project]_guiones la lista de todos
# los guiones que pertenecen al proyecto.
def xml_to_db_guion(fileXML, ci_project):
    # lee el archivo xml
    with open(fileXML) as file:
        xml_data = file.read()

    # Extrae el nombre del archivo
    name_xml = os.path.basename(fileXML)

    # Crea una instancia de BeautifulSoup
    soup = BeautifulSoup(xml_data, features="xml")

    # Extrae los datos para la tabla del [ci_project]_guiones
    titulo = soup.find("titulo").text
    episodio = soup.find("episodio").text
    capitulo = soup.find("cap").text

    creditos = soup.find_all("creditos") 

    # Datos dentro de las etiquetas <credito>
    dialogos = creditos[1].text.strip()
    argumento = creditos[3].text.strip()
    edicion = creditos[5].text.strip()
    vers = creditos[8].text.strip()
    vers = vers.replace("(", "").replace(")","")

    # Concatena el titulo el numero de episodio y la version para obtener un id codificado.
    data = titulo + episodio + vers
    id = format(zlib.adler32(data.encode()), '08x')

    # el titulo es la concatenación del titulo y del episodio
    titulo = f"{titulo} - {episodio}"

    data_guiones = [id, titulo, capitulo, dialogos, argumento, edicion, vers, name_xml]
    registro_db = Files.guiones(data_guiones, ci_project)

    return registro_db

# Función para añadir a la tabla [ci_project]_sequences las descripciones 
# de cada secuencia del proyecto.
def xml_to_db_sequences(fileXML, ci_project):
    def count_pages(part):
        lineas = 0

        for line in part.contents:
            if line != '\n': lineas += 1

        for child in part.find_all():
            chars = child.get('size')
            if chars and int(chars) > 48:
                many_lines = math.floor(int(chars) / 48)
                lineas += many_lines

        octavos = round(lineas/4)
        if octavos == 0: octavos = 1

        return octavos
    
    def extract_data(sec):
        id = f"{sec.cap.text}{sec.num.text}"
        cap = sec.cap.text
        num = sec.num.text
        loc = sec.loc.text
        ubc = sec.ub.text
        amb = (sec.amb.text).replace("\xa0", "")
        return [id, cap, num, loc, ubc, amb]
    
    # lee el archivo xml
    with open(fileXML) as file:
        xml_data = file.read()

    # Crea una instancia de BeautifulSoup
    soup = BeautifulSoup(xml_data, features="xml")
    count = 0
    flag_error = False
    for part in soup.find_all("part"):
        capitulo = part.sec.cap
        
        if capitulo:
            sec_data = extract_data(part.sec)
            sec_data.insert(1, count)
            sec_data.append(count_pages(part))
            sec_data.append('')
            sec_data.append(False)
            add_sec = Files.sequences(sec_data, ci_project) 
            print(sec_data)
            if add_sec['success'] == False:
                flag_error = True
            count += 1
    
    if flag_error == False:
        return {"message": "Los datos han sido añadidos con exito.", "success": True}
    else:
        return {"message": "Ha habido un error al añadir los datos.", "success": False}

# Función para añadir a la tabla [ci_project]_cast donde se almacenan 
# la lista de los personajes que intervienen en el proyecto.
def xml_to_db_perx(fileXML, ci_project):

    with open(fileXML) as file:
            xml_data = file.read()

    # Crea una instancia de BeautifulSoup
    soup = BeautifulSoup(xml_data, features="xml")

    interpretan = soup.find_all('perx')

    # Crea un diccionario para los personajes { 'perdonaje': num_caracteres_dialogo }
    dic_per = {}

    # Lista los personajes que aparecen en cada secuencia.
    for personajes in interpretan:
        lista_personajes = personajes.text.split(", ")
        for personaje in lista_personajes:
            personaje = personaje.replace("(", "").replace(" OFF)", "")
            dic_per[personaje] = 0

    # Busca los dialogos del guion.
    dialogos = soup.find_all('dlg')

    # Extrae los nombres de los personajes con texto en los dialogos.
    for dialogo in dialogos:
        per = dialogo.per.text
        per = per.replace("(", "").replace("OFF)", "")

        # Añade como valor de cada personaje el tamaño en caracteres de su texto
        # Este valor se actualiza con cada linea de dialogo.
        try:
            size_dlg = dic_per[per]
            suma_dlg = size_dlg + int(dialogo['size'])
            dic_per[per] = suma_dlg
        except:
            # Si el personaje no está definido como interprete no se tiene en cuenta su texto.
            # Ejemplo: puede aparecer un TODOS como personaje. En este caso se excluye aunque tiene texto.
            print(per)

    # Borra los personajes que no tienen texto en los dialogos. 
    del_items = [clave for clave, valor in dic_per.items() if valor == 0]
    for clave in del_items:
        del dic_per[clave]
    
    # Ordena el diccionario de mayor valor a menor.
    # Esto sirve para el nc (numero de personaje)
    sorted_dic = dict(sorted(dic_per.items(), key=lambda x: x[1], reverse=True))

    # Sustituye el numero de caracteres de cada perosonaje por un id para la base de datos.
    # El id es una codificación del nombre.
    for nombre in sorted_dic:
        id = format(zlib.adler32(nombre.encode()), '08x')
        sorted_dic[nombre]=id

    # Envía el diccionario a la base de datos.
    consulta = Files.casting(sorted_dic, ci_project)

    if consulta["success"] == True:
        return {"message": consulta["message"], "success": True}
    else:
        return {"message": f"Error al introducir los datos en la tabla {ci_project}_cast", "success": False}

   
from bs4 import BeautifulSoup
import re, zlib, os

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

                    elif item != "INTERCUT" and seclist.index(item) > 2:
                        amb += item
                        
                fileXML.write("<sec><cap>"+cap+"</cap><num>"+num+"</num><loc>"+loc.strip()+"</loc><ub>"+ub.strip()+"</ub><amb>"+amb.strip()+"</amb></sec>\n")
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

def xml_to_db_guion(fileXML):
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

    return [id, titulo, capitulo, dialogos, argumento, edicion, vers, name_xml]
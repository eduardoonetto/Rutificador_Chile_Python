# @author @eduardoonetto https://github.com/eduardoonetto/Rutificador_Chile_Python

import requests,urllib3, sys, locale
from bs4 import BeautifulSoup
import json

def limpia_guion(Run):
    if int(Run.find("-")) > 0:
        position = Run.index("-")
        Run = Run[0:position]
        return Run
    else:
        return Run

def coloca_puntos(Run):
    if Run.find("."):
        Run = Run.replace(".", "")
    locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
    Run = locale.format_string('%d', int(Run), 1)
    return Run    

def envia_y_limpia(rut):
    urllib3.disable_warnings()
    s=requests.Session()
    s.headers.update(headers)
    r=s.post(URL+rut)
    soup=BeautifulSoup(r.content,"html.parser")
    data = []
    table_body = soup.find('tr')
    data = str(table_body.findAll('td'))
    data = data.replace("<td>", '')
    data = data.replace("</td>", '')
    data = data.replace("[", '')
    data = data.replace("]", '')
    data = data.split(",")
    return data
try:
    #Envio POST a:
    URL = "https://r.rutificador.co/pr/"

    # Get args from command line
    Run=sys.argv[1]

    headers={
        "Content-Type" : "application/x-www-form-urlencoded",
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
    }

    # Web scraping rutificador
    data = envia_y_limpia(Run)

    # Necesito estos datos
    keys = ["nombre", "run", "sexo", "direccion_servel", "circunscripcion_electoral", "comuna"]
    # Recorrer datos y transformarlos a diccionario
    datos_servel = {}
    count = 0
    for k in keys:
        datos_servel[k] = str(data[count]).strip()
        count += 1

    # Datos a devolver
    print(json.dumps(datos_servel))

except NameError:
    print(f"Uso: python rutificador.py [00000000-0 || 00000000 || 00.000.000-0 || 00.000.000]")
except IndexError:
    print(f"Sin informacion para el Rut: {run_origen}")
except ValueError:
    print(f"{run_origen} No tiene el valor esperado.")
except Exception as e:
    print(f"Error inesperado:", e)

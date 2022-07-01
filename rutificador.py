import requests,urllib3, sys, locale
from bs4 import BeautifulSoup

#Uso python rutificador.py [19746549-2 || 19746549 || 19.746.549-2 || 19.746.549]

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

def envia_y_limpia(data):
    urllib3.disable_warnings()
    s=requests.Session()
    s.headers.update(headers)
    r=s.post(URL, data=data)
    soup=BeautifulSoup(r.content,"html.parser")
    #print(soup)
    data = []
    table = soup.find('table')
    #print(table)
    table_body = table.findAll('tr')[1]
    #print(table_body)
    data = str(table_body.findAll('td'))
    data = data.replace("<tr>", '')
    data = data.replace("</tr>", '')
    data = data.replace("</td>", '')
    data = data.replace("<td>", '')
    data = data.replace("[", '')
    data = data.replace("]", '')
    data = data.split(",")
    return data
try:
    #Envio POST a:
    URL = "https://rutificador.org/backend.php"
    # Necesito estos datos
    head = ["Run", "Nombre", "Sexo", "Direccion Servel", "Ciudad"]

    run_origen = None
    Run=sys.argv[1]
    
    headers={
        "Content-Type" : "application/x-www-form-urlencoded",
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
            }

    #guardar dato sin formatear
    run_origen = Run
    Run = limpia_guion(Run)
    Run = coloca_puntos(Run)

    data={
        "rut": Run,
        "action": "search_by_rut"
        }

    data = envia_y_limpia(data)

    count = 0
    for h in head:
        print(f"{h} : {data[count]}")
        count += 1
except NameError:
    print(f"Uso: python rutificador.py [00000000-0 || 00000000 || 00.000.000-0 || 00.000.000]")
except IndexError:
    print(f"Sin informacion para el Rut: {run_origen}")
except ValueError:
    print(f"{run_origen} No tiene el valor esperado.")
except Exception as e:
    print(f"Error inesperado:", e)

import requests
from lxml import html
import pandas as pd

# Realiza la solicitud GET
url = 'https://pln.puertovalparaiso.cl/pln/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ga_1EEVGMY6FL=GS1.1.1725248453.4.0.1725248453.0.0.0; _ga=GA1.2.809094402.1724901886; _gid=GA1.2.1808057673.1725248454; csrftoken=Pajjeqn3XaZ58ZFObRea9qnBISNIhLsu',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

response = requests.get(url, headers=headers, verify=False)

# Asegúrate de que la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML
    tree = html.fromstring(response.content)

    # Utilizar XPath para extraer la tabla
    table = tree.xpath('//*[@id="main"]/div[2]/div[2]/table')

    # Definir los encabezados de la tabla
    headers = ['Nave.', 'T', 'Anuncio', 'Vacio'] 
    
    # Extraer datos de la tabla
    extracted_data = []
    for row in table[0].xpath('.//tr'):
        print(row, 'row')
        row_data = [cell.text_content().strip() for cell in row.xpath('.//td')]
        if len(row_data) > 0:  # Ignora las filas vacías
            extracted_data.append(row_data)

    # Crear el DataFrame de pandas
    df = pd.DataFrame(extracted_data, columns=headers)

    # Mostrar la tabla
    print(df)
else:
    print(f"Error en la solicitud: {response.status_code}")

import requests
from lxml import html
import pandas as pd

# Realiza la solicitud GET
url = 'https://gessup.puertosanantonio.com/Planificaciones/general.aspx'
headers = {
    'Host': 'gessup.puertosanantonio.com',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'es-ES',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive'
}

response = requests.get(url, headers=headers)

# Asegúrate de que la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML
    tree = html.fromstring(response.content)
    data = tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_GridView_Lista"]')

    # Definir los encabezados de la tabla
    headers = ['E.T.A.', 'Agencia', 'Nave', 'Eslora', 'Terminal', 'Emp. muellaje', 'Carga', 'Detalle', 'Cantidad', 'Operación']
    
    # Extraer y procesar la información
    extracted_data = []
    for table in data:
        for row in table.xpath('.//tr'):
            row_data = [cell.text_content().strip() for cell in row.xpath('.//td')]
            if len(row_data) > 0:  # Ignora las filas vacías
                extracted_data.append(row_data)

    # Crear el DataFrame de pandas
    df = pd.DataFrame(extracted_data, columns=headers)

    # Mostrar la tabla
    print(df)
else:
    print(f"Error en la solicitud: {response.status_code}")

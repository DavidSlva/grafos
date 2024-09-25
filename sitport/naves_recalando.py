import requests
import json
from colorama import Fore, Style, init

# Inicializar colorama para colores en la consola
init(autoreset=True)

# Definir la URL y los headers
url = "https://orion.directemar.cl/sitport/back/users/consultaNaveRecalando"
headers = {
    "Host": "orion.directemar.cl",
    "Content-Length": "2",
    "Sec-Ch-Ua": '"Not(A:Brand";v="24", "Chromium";v="122"',
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Origin": "https://sitport.directemar.cl",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://sitport.directemar.cl/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "es-419,es;q=0.9",
    "Priority": "u=1, i",
    "Connection": "close"
}

# Definir el cuerpo de la solicitud
data = {}

# Realizar la solicitud POST
response = requests.post(url, headers=headers, json=data)

# Imprimir el estado de la respuesta
print(f"{Fore.CYAN + Style.BRIGHT}Status Code: {Fore.GREEN + Style.BRIGHT}{response.status_code}")

# Intentar formatear la respuesta como JSON si es posible
try:
    response_json = response.json()  # Parsear la respuesta a JSON
    formatted_json = json.dumps(response_json, indent=4, ensure_ascii=False)  # Formatear con indentación
    print(f"{Fore.CYAN + Style.BRIGHT}Response JSON:\n{Fore.YELLOW + Style.NORMAL}{formatted_json}")
except ValueError:
    # Si no es un JSON válido, simplemente imprime el texto de la respuesta
    print(f"{Fore.CYAN + Style.BRIGHT}Response Text:\n{Fore.YELLOW + Style.NORMAL}{response.text}")

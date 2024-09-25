import requests

url = "https://orion.directemar.cl/sitport/back/users/consultaNavezarpe"

headers = {
    "Host": "orion.directemar.cl",
    "Content-Length": "2",
    "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
    "Accept": "application/json, text/plain, */*",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "es-ES",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
    "Content-Type": "application/json",
    "Origin": "https://sitport.directemar.cl",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://sitport.directemar.cl/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
    "Connection": "keep-alive"
}

data = "{}"  # Payload de la solicitud en formato JSON

response = requests.post(url, headers=headers, data=data, verify=False)

print(response.status_code)
print(response.text)

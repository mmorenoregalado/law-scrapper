import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import json

base_url = 'https://www.congresochihuahua.gob.mx/biblioteca/leyes/index.php?pag={page_num}&palabra=#divResultados'
page_num = 1
laws = []

while True:
    url = base_url.format(page_num=page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', {'class': 'table table-bordered'})

    # Si no hay más tablas, asumimos que hemos llegado al final de las páginas
    if not tables:
        break

    print(f"Procesando la página {page_num}...")

    for table in tables:
        law_name = table.find('th').text if table.find('th') else None
        law_link = table.find('a', href=True)['href'] if table.find('a', href=True) else None
        law_date = table.find('b').text.replace('Publicación:', '').strip() if table.find('b') else None

        if law_name and law_link:
            laws.append({
                'name': law_name,
                'link': law_link,
                'date': law_date
            })

    page_num += 1

# Guarda el resultado en un archivo JSON
with open('laws.json', 'w') as f:
    json.dump(laws, f)

print("Los datos se han guardado en 'laws.json'")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from io import StringIO

# Eurovaistine, nereceptiniai vaistai, nuo persalimo

products_data = []
for i in range(1, 6):
    url = f"https://www.eurovaistine.lt/vaistai-nereceptiniai/persalimui?page={i}"
    response = requests.get(url)
    html_content = response.text
    # print(response.status_code)

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup)
    products = soup.find_all('div', class_='productCard')
    for product in products:
        gamintojas = product.find('div', class_='brand mt-0').text.strip()
        pavadinimas = product.find('div', class_='title').text.strip()
        kaina = product.find('div', class_='productPrice text-end').text.strip().replace(' €', '')
        likutis = product.find('div', class_='soldOut').text.strip()

        products_data.append({
            'Gamintojas': gamintojas,
            'Pavadinimas': pavadinimas,
            'Kaina': kaina,
            'Likutis': likutis
        })



json_data = json.dumps(products_data)

# Naudojamas StringIO konvertuoti JSON tekstą į objektą, panašų į failą
json_data_io = StringIO(json_data)

# Konvertuojami JSON duomenys į DataFrame
df = pd.read_json(json_data_io)

# Išsaugomi DataFrame duomenys į CSV failą
df.to_csv('eurovaistine.csv', index=False)
print("Duomenys išsaugoti į 'eurovaistine.csv' failą.")






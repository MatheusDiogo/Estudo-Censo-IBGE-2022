import requests
import pandas as pd
import json

dados_pop = pd.read_excel('Censo 2022 IBGE - MUNICIPIOS.xlsx', dtype={"id_municipio": str})

#Iniciando extração de dados das malhas
url_malhas = 'https://servicodados.ibge.gov.br/api/v3/malhas/municipios/'
print('Extraindo dados de malhas!')

lista_municipios = list(dados_pop['id_municipio'].unique())

# Inicializar a variável geo_json fora do loop
geo_json = None

for municipio in lista_municipios:
    try:
        response = requests.get(url=url_malhas + str(municipio) + '?formato=application/vnd.geo+json')

        if response.status_code == 200:
            # Carregar os dados GeoJSON para o município atual
            municipio_geo_json = response.json()
            
            # Atualizar geo_json para incluir os dados do município atual
            if geo_json is None:
                geo_json = municipio_geo_json
            else:
                # Fundir as propriedades de feature do novo GeoJSON ao GeoJSON existente
                geo_json['features'].extend(municipio_geo_json['features'])

    except Exception as e:
        print(f"Erro ao processar município {municipio}: {e}")

# Salvar os dados GeoJSON em um arquivo
with open('geo_json_data.json', 'w') as f:
    json.dump(geo_json, f, indent=4)
    print('Dados de geo_json salvos com sucesso em geo_json_data.txt')
    print(geo_json['features'][0])
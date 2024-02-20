import requests
import pandas as pd

url = 'https://servicodados.ibge.gov.br/api/v3/agregados/9522/periodos/2022/variaveis/93|6318|614?localidades=N6[1100023,1100031]'
dados = requests.get(url=url).json()
print(dados)
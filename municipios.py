import requests
import pandas as pd

url = 'https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/-6/variaveis/93?localidades=N6[1100015,1100023,1100031,2611309,2611606]&classificacao=2[4,5]|287[100362,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094,93095,93096,93097,93098,49108,49109]'

response = requests.get(url=url)

if response.status_code == 200:
    dados = pd.json_normalize(data=response.json(), record_path=['resultados'], meta=['variavel', 'unidade'])
    print('Dados extraídos com sucesso!')
    resultados = dados.explode('series').reset_index(drop=True)
    classificacoes = pd.json_normalize(resultados['classificacoes'])
    localidades = pd.json_normalize(resultados['series'])
    final_data = pd.concat([classificacoes, localidades], axis=1)
    final_data['Sexo'] = final_data[0].apply(lambda x: list(x.values())[2])
    final_data['Idade'] = final_data[1].apply(lambda x: list(x.values())[2])
    final_data.drop(columns=[0, 1, 2, 'localidade.nivel.id'], inplace=True)
    final_data.rename(columns={'localidade.id': 'id_municipio', 'localidade.nome': 'nome_municipio', 'serie.2022': 'Populacao'}, inplace=True)
else:
    print('Erro', response.status_code)

id_localidade = []
municipio = []
populacao = []


print(final_data)
import requests
import pandas as pd

url = 'https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6[N2[1]]&classificacao=2[4,5]|287[93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094,93095,93096,93097,93098,49108,49109,60040,60041,6653]'

response = requests.get(url=url)

if response.status_code == 200:
    dados = pd.json_normalize(data=response.json(), record_path=['resultados'])
    print('Dados extraídos com sucesso!')
else:
    print('Erro', response.status_code)

sexos = []
cidade = []
idade = []
valor = []

for index, row in dados.iterrows():
    categorias = row['classificacoes']
    sexos.append(list(next((classificacao['categoria'] for classificacao in categorias if 'categoria' in classificacao), None).values())[0])
    idade.append(list(next((classificacao['categoria'] for classificacao in categorias[1:]), None).values())[0])

    series = row['series']
    cidade.append(next((classificacao['localidade']['nome'] for classificacao in series if 'localidade' in classificacao and 'nome' in classificacao['localidade']), None))
    valor.append(int(next((classificacao['serie']['2022'] for classificacao in series if 'serie' in classificacao and '2022' in classificacao['serie']), None)))

df = pd.DataFrame({'Cidade': cidade, 'Sexo': sexos, 'Idade': idade, 'Valor': valor})
print(df)

print(f'População Total entre 15 e 49 anos: {df['Valor'].sum()}')
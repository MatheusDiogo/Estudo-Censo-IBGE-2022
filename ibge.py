import requests
import pandas as pd

# Fazendo a solicitação HTTP e convertendo a resposta para JSON
dados = requests.get(url='https://servicodados.ibge.gov.br/api/v3/agregados/1209/periodos/2022/variaveis/606?localidades=N3[all]&classificacao=58[all]').json()

# Lista para armazenar os dados
populacao_por_idade = []

# Iterando sobre os dados obtidos da API e estruturando os dados
for item in dados:
    for resultado in item['resultados']:
        categoria = resultado['classificacoes'][0]['categoria']
        for uf_data in resultado['series']:
            estado = uf_data['localidade']['nome']
            for ano, valor in uf_data['serie'].items():
                populacao_por_idade.append({
                    'Estado': estado,
                    'Ano': ano,
                    'Grupo de Idade': categoria[list(categoria.keys())[0]],
                    'População': valor
                })

# Criando o DataFrame
df = pd.DataFrame(populacao_por_idade)

# Salvando dados em planilha
df.to_excel('Censo 2022 IBGE.xlsx', index=False)
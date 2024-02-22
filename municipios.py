import requests
import pandas as pd

# URL's das Regiões
urls = {
    'Norte': 'https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6[N2[1]]&classificacao=2[4,5]|287[100362,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094]',
    'Nordeste': 'https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6[N2[2]]&classificacao=2[4,5]|287[100362,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094]',
    'Sudeste': 'https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6[N2[3]]&classificacao=2[4,5]|287[100362,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094]',
    'Sul': 'https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6[N2[4]]&classificacao=2[4,5]|287[100362,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094]',
    'Centro_Oeste': 'https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6[N2[5]]&classificacao=2[4,5]|287[100362,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094]'
}

dados_pop = pd.DataFrame()

# Iterar sobre as URLs
for regiao, url in urls.items():
    response = requests.get(url=url)

    if response.status_code == 200:
        # Normalizando Json
        dados = pd.json_normalize(data=response.json(), record_path=['resultados'], meta=['variavel', 'unidade'])
        print('Dados extraídos com sucesso!')
        
        # Extraindo dados das localidades que vamos usar
        resultados = dados.explode('series').reset_index(drop=True)
        classificacoes = pd.json_normalize(resultados['classificacoes'])
        localidades = pd.json_normalize(resultados['series'])
        final_data = pd.concat([classificacoes, localidades], axis=1)
        final_data['Sexo'] = final_data[0].apply(lambda x: list(x.values())[2])
        final_data['Idade'] = final_data[1].apply(lambda x: list(x.values())[2])
        
        # Aplicando transformações nos dados
        final_data.drop(columns=[0, 1, 2, 'localidade.nivel.id'], inplace=True)
        final_data.rename(columns={'localidade.id': 'id_municipio', 'localidade.nome': 'nome_municipio', 'serie.2022': 'Populacao'}, inplace=True)
        final_data['Regiao'] = regiao
        dados_pop = pd.concat([dados_pop, final_data], ignore_index=True)
    else:
        print('Erro', response.status_code)

url_densidade = 'https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/6318?localidades=N6[N2[1,2,3,4,5]]'

response = requests.get(url=url_densidade)

if response.status_code == 200:
    # Normalizando Json
    dados_densidade = pd.json_normalize(data=response.json(), record_path=['resultados'], meta=['variavel', 'unidade'])
    resultados_densidade = dados_densidade.explode('series').reset_index(drop=True)
    
    # Extraindo dados das localidades que vamos usar
    classificacoes_densidade = pd.json_normalize(resultados_densidade['classificacoes'])
    localidades_densidade = pd.json_normalize(resultados_densidade['series'])
    densidade = pd.concat([classificacoes_densidade, localidades_densidade], axis=1)
    
    # Removendo outros niveis de teritorio
    densidade = densidade.loc[densidade['localidade.nivel.nome'] == 'Município']
    
    # Aplicando transformações nos dados
    densidade.rename(columns={'localidade.id': 'id_municipio', 'serie.2022': 'Area (km²)'}, inplace=True)
    area_km2 = densidade[['id_municipio', 'Area (km²)']]

#Salvando dados em xlsx
area_km2.to_excel('Área Territorial - MUNICIPIOS.xlsx', index=False)
dados_pop.to_excel('Censo 2022 IBGE - MUNICIPIOS.xlsx', index=False)
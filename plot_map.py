import plotly.express as px
import pandas as pd
import json

densidade = pd.read_excel('Área Territorial - MUNICIPIOS.xlsx', dtype={"id_municipio": str})
dados = pd.read_excel('Censo 2022 IBGE - MUNICIPIOS.xlsx', dtype={"id_municipio": str})

# Converte a coluna 'Populacao' para numérica, substituindo valores não numéricos por NaN
dados['Populacao'] = pd.to_numeric(dados['Populacao'], errors='coerce')

# Substitui os valores NaN por 0 na coluna 'Populacao'
dados['Populacao'].fillna(0, inplace=True)

# Desconsiderando Faixas de Idade
dados_populacao = dados[dados['Idade'] == 'Total']

# Merge entre densidade e população dos municipios
municipios = pd.merge(dados_populacao, densidade, on='id_municipio')
municipios['densidade_demografica'] = municipios['Populacao'] / (municipios['Area (km²)'])

# Extraindo dados de malhas
with open('geo_json_data.json') as file:
    geo_json = json.load(file)

# Criar o mapa coroplético usando Plotly Express
fig = px.choropleth_mapbox(
    data_frame=municipios,
    geojson=geo_json,
    locations='id_municipio',  # Coluna que contém os códigos dos municípios
    featureidkey='properties.codarea',
    color='densidade_demografica',  # Coluna que define a cor do mapa
    color_continuous_scale='thermal',  # Esquema de cores contínuo
    range_color=(municipios['densidade_demografica'].min(), municipios['densidade_demografica'].quantile(0.95).max()),
    mapbox_style='open-street-map',
    zoom=3.5,
    center={"lat": -20, "lon": -60},
    opacity=1,
    labels={'Populacao': 'População', 'densidade_demografica': 'Densidade Demografica'},
    width=1200,
    height=800,
    title='População por Município',  # Título do mapa
    hover_name='nome_municipio',  # Nome exibido ao passar o mouse sobre os polígonos
    hover_data={'id_municipio': False, 'Populacao': True, 'densidade_demografica': True}  # Exibir informações adicionais no hover
)

# Personalizar escala
fig.update_layout(
    margin={'r': 0, 't': 1, 'l': 0, 'b': 1},
    coloraxis_colorbar={
        'title': {
            'text': 'Densidade Demografica',
            'side': 'right'
        }
    }
)

# Customize the individual polygons
fig.update_geos(
    showcoastlines=False,  # Hide coastlines
    visible=False  # Hide geographical boundaries
)

# Update marker settings
fig.update_traces(
    marker_line_width=0.05,
    selector=dict(type='choroplethmapbox')
)

# Exibir o mapa
fig.show()

fig.write_html("pop_ibge_map_2022.html")
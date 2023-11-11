# Importação livrarias
import plotly.express as px
from haversine import haversine

# Importação das bibliotecas
import pandas as pd
import inflection
import folium as fl
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

#Exibir a página no formato tela cheia
st.set_page_config(layout="wide")

# ------------------------------------------------------
# Leitura do arquivo .csv
# ------------------------------------------------------

df = pd.read_csv('../datasets/zomato.csv')

# ------------------------------------------------------
# Funções
# ------------------------------------------------------


def rename_columns(dataframe):
    """Está função tem a responsabilidade de normatizar os nomes das colunas """
    df = dataframe.copy()
    def title(x): return inflection.titleize(x)
    def snakecase(x): return inflection.underscore(x)
    def spaces(x): return x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


def country_name(country_id):
    """Está função tem a resposabilidade de alterar o código das cidades
    (country_code) pelo nome escrito"""
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "USA",
    }

    return COUNTRIES[country_id]


def create_price_type(price_range):
    """Altera o tipo de comida (Barato, Caro, Normal ou Gourmet)
    conforme a range de preço (price_range)"""
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


def color_name(color_code):
    """Função responsável por colocar o nome da cor e conforme seu código"""
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }
    return COLORS[color_code]

# ------------------------------------------------------
# Limpeza do dataframe
# ------------------------------------------------------


# Fazendo a normatização dos nomes das colunas
df1 = rename_columns(df)

# remove as linhas duplicadas
df1 = df1.drop_duplicates().reset_index(drop=True)

# Cria a coluna 'Country' com os nomes das cidades conforme seu "coutry_code"
df1['country'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))

# Cria a coluna que categoriza o tipo de comida conforme a range de preço
df1['price_type'] = df1.loc[:, 'price_range'].apply(
    lambda x: create_price_type(x))

# Cria a coluna com os nomes das cores conforme o 'rating_color'
df1['name_color'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))

# Altera a coluna 'cuisines' para <str> e o tipo de cozinha para apenas um
df1["cuisines"] = df1.loc[:, "cuisines"].astype(
    str).apply(lambda x: x.split(",")[0])

# limpar 'nan' de cuisines
selectnan = df1['cuisines'] != 'nan'
df1 = df1.loc[selectnan, :].reset_index(drop=True)

# Copia do df para os "Nossos Números"
df_num = df1.copy()

# --------------------------------------------------------------
# BARRA LATERAL
# --------------------------------------------------------------

# Importação logo fome zero
#image_path = 'logo.jpg'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=250)

st.sidebar.header(
    ':orange[FOME ZERO - Um restaurante para cada tipo de fome.]', divider='orange')

#----------------Multiselect---------------------------------
# Cria a lista com os nomes dos paises para o multiselect
nome_paises = df1['country'].unique().tolist()

# Cria o filtro de opções para escolha do país no mapa
options_pais = st.sidebar.multiselect(
    'Escolha um ou mais paises que deseja consultar os restaurantes.',
    nome_paises, ['Brazil', 'England', 'Qatar', 'South Africa',
                  'Canada', 'Australia'])

# Filtro de paises
select_lin = df1['country'].isin(options_pais)
df1 = df1.loc[select_lin, :]

# --------------------------------------------------------------
# LAYOUT STREAMLIT
# --------------------------------------------------------------

st.header(':orange[FOME ZERO!]')
st.subheader(
    ':orange[Um restaurante para cada tipo de fome!]', divider='orange')
st.subheader(':orange[Os Números da empresa Hoje!]')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    quantidade_rest = len(df_num.loc[:, 'restaurant_id'].unique())
    col1.metric('Restaurantes', quantidade_rest)

with col2:
    quantidade_pais = len(df_num.loc[:, 'country'].unique())
    col2.metric('Paises', quantidade_pais)

with col3:
    quantidade_cidades = len(df_num.loc[:, 'city'].unique())
    col3.metric('Cidades', quantidade_cidades)

with col4:
    quantidade_avaliacoes = df_num['votes'].sum()
    col4.metric('Avaliações', quantidade_avaliacoes)

with col5:
    quantidade_culinarias = len(df_num['cuisines'].unique())
    col5.metric('Tipos Cozinhas', quantidade_culinarias)

with st.container():
    st.header('Mapa dos restaurantes')
    
    # Agrupar informações para o mapa
    df_map = (df1.loc[:, ['country', 'city', 'cuisines', 'aggregate_rating', 'average_cost_for_two', 'name_color','currency',
                          'restaurant_name', 'latitude', 'longitude']]
                          .groupby(['country', 'city', 'cuisines', 'aggregate_rating',
                                    'average_cost_for_two', 'name_color', 'restaurant_name','currency'])
                          .median()
                          .reset_index())

    # Plotar o Mapa
    map = fl.Map(control_scale=True)

    # Mostra os icones do mapa agrupados "clusters"
    mc = MarkerCluster().add_to(map)

    # For para percorrer todo o "df" e colocar as marcações no map
    for index, location_info in df_map.iterrows():
        # Cria o popup html para uma melhor formatação do texto no popup do map
        html = '''
        <p><b>{nome}</b></p>
        <b>Preço p/ 2 pessoas: {preco}</b><br>
        <b>Moeda local: {moeda}</b><br>
        <b>Tipo de Culinária: </b>{tipo}<br>
        <b>Avaliação: </b>{voto}
        '''.format(nome=location_info['restaurant_name'],preco=location_info['average_cost_for_two'],
                 moeda=location_info['currency'],tipo=location_info['cuisines'],voto=location_info['aggregate_rating'])
        
        # Criar as marcações no mapa
        fl.Marker([location_info['latitude'], location_info['longitude']],
                  popup=fl.Popup(html, parse_html=False,
                                 min_width=200, max_width=200),
                  icon=fl.Icon(icon='house',
                               prefix='fa',
                               color=location_info['name_color'],
                               icon_color='white')).add_to(mc)
    folium_static(map, width=1024, height=600)

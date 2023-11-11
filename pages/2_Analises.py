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

# Exibir a página no formato tela cheia
st.set_page_config(layout="wide")

# ------------------------------------------------------
# Leitura do arquivo .csv
# ------------------------------------------------------
df = pd.read_csv('datasets\zomato.csv')

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

# --------------------------------------------------------------
# BARRA LATERAL
# --------------------------------------------------------------

# Importação logo fome zero
#image_path = 'logo.jpg'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=250)

st.sidebar.header(
    ':orange[FOME ZERO - Um restaurante para cada tipo de fome.]', divider='orange')

#----------------Slider-----------------------------------------
qtd = st.sidebar.slider('Selecione a quantidade de restaurantes',1,20, value=10)

#----------------Multiselect-----------------------------------------
# Cria a lista com os nomes dos paises para o multiselect
nome_paises = df1['country'].unique().tolist()

# Cria o filtro de opções para escolha do país no mapa
options_pais = st.sidebar.multiselect(
    'Escolha um ou mais paises que deseja consultar os restaurantes.',
    nome_paises, ['USA', 'India', 'South Africa', 'Philippines', 'England', 'New Zeland'])

# Filtro de paises
select_lin = df1['country'].isin(options_pais)
df1 = df1.loc[select_lin, :]



# --------------------------------------------------------------
# LAYOUT STREAMLIT
# --------------------------------------------------------------
st.header(':orange[FOME ZERO!]')
st.subheader(
    ':orange[Um restaurante para cada tipo de fome!]', divider='orange')

tab1, tab2, tab3, tab4 = st.tabs(
    [':world_map: Paises', ':city_sunset: Cidades', ':pie: Restaurantes', ':takeout_box: Tipos de Cozinha.'])

# --------------------------------------------------------------
# VISÃO PAISES
# --------------------------------------------------------------
with tab1:
    st.title(':orange[Gráficos - Nossos Números Por País.]')

    with st.container():
        df_aux2 = (df1.loc[:, ['country', 'restaurant_id']].groupby('country')
                                                           .nunique()
                                                           .sort_values('restaurant_id', ascending=False)
                                                           .reset_index())

        fig = px.bar(df_aux2, x='country', y='restaurant_id', color='restaurant_id', title='QUANTIDADE DE RESTURANTES POR PAÍS',
                     height=600, width=1000, text='restaurant_id', labels={'restaurant_id': 'Restaurantes'})
        fig.update_xaxes(title='Países', title_font_color='white',
                         ticks='outside', tickfont_color='White')
        fig.update_yaxes(title='Quantidade de Restaurantes',
                         title_font_color='white', ticks='outside', tickfont_color='black')
        fig.update_traces(marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5)
        st.plotly_chart(fig, use_conteiner_widt=True)

    with st.container():
        cols1, cols2 = st.columns(2)

        with cols1:
            df_aux1 = (df1.loc[:, ['country', 'city']].groupby('country')
                                                      .nunique()
                                                      .sort_values('city', ascending=False)
                                                      .reset_index())

            # df_aux = df_aux.head(5)
            fig = px.bar(df_aux1, x='country', y='city', color='city', title='QUANTIDADE DE CIDADES POR PAÍS',
                         height=500, width=500, text='city', labels={'city': 'Cidades'})
            fig.update_xaxes(title='Países', title_font_color='white',
                             ticks='outside', tickfont_color='white')
            fig.update_yaxes(title='Quantidade de Cidades',
                             title_font_color='white', ticks='outside', tickfont_color='white')
            fig.update_traces(
                marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
            st.plotly_chart(fig, use_conteiner_widt=True)

        with cols2:
            df_aux8 = (df1.loc[:, ['country', 'votes']].groupby('country')
                                                       .mean()
                                                       .sort_values('votes', ascending=True)
                                                       .reset_index())

            fig = px.bar(df_aux8, x='country', y='votes', color='votes', title='MÉDIA DE AVALIAÇÕES P/ PAÍS',
                         height=500, width=500, text='votes', labels={'votes': 'Avaliações'})
            fig.update_xaxes(title='Paises', title_font_color='white',
                             ticks='outside', tickfont_color='white')
            fig.update_yaxes(title='Avaliações', title_font_color='white',
                             ticks='outside', tickfont_color='white')
            fig.update_traces(
                marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
            st.plotly_chart(fig, use_conteiner_widt=False)

    with st.container():
        df_aux11 = (df1.loc[:, ['country', 'average_cost_for_two']].groupby('country')
                                                                   .mean()
                                                                   .sort_values('average_cost_for_two', ascending=False)
                                                                   .reset_index())

        fig = px.bar(df_aux11, x='country', y='average_cost_for_two', title='MÉDIA DE PREÇO DO PRATO P/ 2 PESSOAS',
                     height=600, width=1000, text='average_cost_for_two')
        fig.update_xaxes(title='Paises', title_font_color='white',
                         ticks='outside', tickfont_color='white')
        fig.update_yaxes(title='Média de Preço', title_font_color='white',
                         ticks='outside', tickfont_color='white')
        fig.update_traces(marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5)
        st.plotly_chart(fig, use_conteiner_widt=False)

# --------------------------------------------------------------
# VISÃO CIDADES
# --------------------------------------------------------------
with tab2:
    st.title(':orange[Gráficos - Nossos Números Por Cidade.]')

    with st.container():
       # Agrupamento por cidade com o groupby.
        df_c1 = (df1.loc[:, ['city', 'country', 'restaurant_id']].groupby(['country', 'city'])
                                                                 .count()
                                                                 .sort_values('restaurant_id', ascending=False)
                                                                 .reset_index())
        # Top 10
        df_c1 = df_c1.head(qtd)

        fig = px.bar(df_c1, x='city', y='restaurant_id', color='country', title=f'TOP {qtd} - Cidades com mais restaurantes cadastrados.',
                     height=600, width=1000, text='restaurant_id', labels={'country': 'Paises'})
        fig.update_xaxes(title='Cidades', title_font_color='white',
                         ticks='outside', tickfont_color='white')
        fig.update_yaxes(title='Número de Restaurantes',
                         title_font_color='white', ticks='outside', tickfont_color='white')
        fig.update_traces(marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5)
        st.plotly_chart(fig, use_conteiner_widt=False)

    with st.container():
        cols1, cols2 = st.columns(2)
        with cols1:
            # Selecionei as cidades com pontuação acima da 4
            select = df1['aggregate_rating'] > 4
            df_aux2 = df1.loc[select, :]

            # Fiz o agrupamento por cidade
            df_c2 = (df_aux2.loc[:, ['country', 'city', 'aggregate_rating']].groupby(['country', 'city'])
                                                                            .count()
                                                                            .sort_values('aggregate_rating', ascending=False)
                                                                            .reset_index())
            # Top 10
            df_c2 = df_c2.head(qtd)

            fig = px.bar(df_c2, x='aggregate_rating', y='city', color='country', 
                         title=f'TOP {qtd}- Restaurantes de avaliação maior 4,0',
                         height=500, width=500, text='aggregate_rating', labels={'country': 'Paises'})
            fig.update_xaxes(title='Número de Restaurantes',
                             title_font_color='white', ticks='outside', tickfont_color='white')
            fig.update_yaxes(title='Cidades', title_font_color='white',
                             ticks='outside', tickfont_color='white')
            fig.update_traces(
                marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
            st.plotly_chart(fig, use_contaner_widt=False)

        with cols2:
            # Selecionei as cidades com pontuação abaixo 2.5
            select = (df1['aggregate_rating'] < 2.5)
            df_aux3 = df1.loc[select, :]

            # Fiz o agrupamento por cidade
            df_c3 = (df_aux3.loc[:, ['country', 'city', 'aggregate_rating']].groupby(['country', 'city'])
                                                                            .count()
                                                                            .sort_values('aggregate_rating', ascending=False)
                                                                            .reset_index())

            # Top 10
            df_c3 = df_c3.head(qtd)

            fig = px.bar(df_c3, x='aggregate_rating', y='city', color='country', 
                         title=f'TOP {qtd} - Restaurantes de avaliação menor 2,5',
                         height=500, width=500, text='aggregate_rating', labels={'country': 'Paises'})
            fig.update_xaxes(title='Número de Restaurantes',
                             title_font_color='white', ticks='outside', tickfont_color='white')
            fig.update_yaxes(title='Cidades', title_font_color='white',
                             ticks='outside', tickfont_color='white')
            fig.update_traces(
                marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
            st.plotly_chart(fig, use_container_width=False)

    with st.container():
        # Agrupei por cidade e pedi para que fosse contado a quantidade de tipos de cozinha por cidade
        df_c5 = (df1.loc[:, ['country', 'city', 'cuisines']].groupby(['country', 'city'])
                                                            .nunique()
                                                            .sort_values('cuisines', ascending=False)
                                                            .reset_index())
        # top 10
        df_c5 = df_c5.head(qtd)

        fig = px.bar(df_c5, x='city', y='cuisines', color='country', title=f'TOP {qtd} - Cidades com maior número culinárias distintas.',
                     height=600, width=1000, text='cuisines', labels={'country': 'Paises'})
        fig.update_xaxes(title='Cidades', title_font_color='white',
                         ticks='outside', tickfont_color='white')
        fig.update_yaxes(title='Tipos de Culináiras', title_font_color='white',
                         ticks='outside', tickfont_color='white')
        fig.update_traces(marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5)
        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------
# VISÃO RESTAURANTES
# --------------------------------------------------------------
with tab3:
    st.title(':orange[Visão Dos Restaurantes.]')

    with st.container():
        st.subheader(f'TOP {qtd} - Restaurantes Mais Bem Avaliados')
        #Selecionei apenas os restaurantes com o valor de nota máxima
        select = df1['aggregate_rating'] == 4.9
        dff = df1.loc[select,:]

        #Fiz o agrupamento pelo ID do restaurante
        dfr2 = (dff.loc[:,['restaurant_id','restaurant_name','country','aggregate_rating']]
                .groupby(['restaurant_id','restaurant_name','country'])
                .max()
                .sort_values('restaurant_id', ascending=True)
                .reset_index()
                .head(qtd))

        dfr2 = dfr2.rename(columns={'restaurant_id':'ID Restaurante','restaurant_name' : 'Nome Restaurante','country' : 'País',
                                   'aggregate_rating' : 'Avaliações'})

        st.dataframe(dfr2, use_container_width=True)

    with st.container():
        # Agrupamento dos restaurante por quantidade de avaliações.
        dfr1 = (df1.loc[:, ['country', 'restaurant_name', 'votes']].groupby(['country', 'restaurant_name'])
                                                                   .median()
                                                                   .sort_values('votes', ascending=False)
                                                                   .reset_index())
        # Top 10
        dfr1 = dfr1.head(qtd)
        fig = px.bar(dfr1, x='restaurant_name', y='votes', color='country', title=f'TOP {qtd} - Restaurantes Mais Votados.',
                     height=600, width=400, text='votes', labels={'country': 'Paises'})
        fig.update_xaxes(title='Nome dos Restaurantes',
                         title_font_color='white', ticks='outside', tickfont_color='white')
        fig.update_yaxes(title='Quantidade de Avaliações',
                         title_font_color='white', ticks='outside', tickfont_color='white')
        fig.update_traces(marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        cols1, cols2 = st.columns(2)

        with cols1:
            # Selecionar os restaurante que recebem pedidos on-line
            select2 = df1['has_online_delivery'] == 1
            tem_pedidos_online = df1.loc[select2, :]

            # Vou agrupar para saber a média de votos deste grupo
            dfrest6_tem = tem_pedidos_online['votes'].mean()

            # Selecionar os restaurante que não recebem pedidos on-line
            select2 = df1['has_online_delivery'] == 0
            nao_tem_pedidos_online = df1.loc[select2, :]

            # Vou agrupar para saber a média de votos deste grupo
            dfrest6_nao_tem = nao_tem_pedidos_online['votes'].mean()
           
            resultado = [['Fazem pedidos online','{:0.2f}'.format(dfrest6_tem)],['Não fazem pedidos online','{:0.2f}'.format(dfrest6_nao_tem)]]
            
            dfres = pd.DataFrame(resultado, columns=['tipo_restaurante', 'media_pedidos'])

            fig = px.pie(dfres, values='media_pedidos', names='tipo_restaurante',title='Comparativo de Quantidade de Avaliações')
            st.plotly_chart(fig, use_container_width=True)

        with cols2:
            #Selecionar os restaurante que tem reservas
            select2 = df1['has_table_booking'] == 1
            tem_reserva = df1.loc[select2,:]

            #Selecionar os restaurante que não tem reservas
            select2 = df1['has_table_booking'] == 0
            nao_tem_reserva = df1.loc[select2,:]

            #Vou agrupar para saber a média de valor do prato para 2 pessoas deste grupo
            dfr7_tem = tem_reserva['average_cost_for_two'].mean()

            #Vou agrupar para saber a média do valor do prato para 2 pessoas deste grupo
            dfr7_nao_tem = nao_tem_reserva['average_cost_for_two'].mean()

            resultado = [['Fazem Reserva','{:0.2f}'.format(dfr7_tem)],
                         ['Não Fazem Reserva','{:0.2f}'.format(dfr7_nao_tem)]]

            dfres7 = pd.DataFrame(resultado, columns=['tipo_restaurante','media_pedidos'])

            fig = px.pie(dfres7, values='media_pedidos', names='tipo_restaurante', title='Comparativo do Valor do Prato Para 2 Pessoas.')
            st.plotly_chart(fig, use_container_width=True)


    with st.container():
        #Selecionar os restaurantes com tipo de culinária japonesa nos Estados Unidos
        select2 = (df1['cuisines'] == 'Japanese') & (df1['country'] == 'USA')
        eua_japanese = df1.loc[select2,:]

        #Contar a média de valor do prato para 2 deste grupo
        dfr8_EUA_comida_japonesa = eua_japanese['average_cost_for_two'].mean()

        #Selecionar os restaurantes com tipo de culinária churrasco(BBQ) nos Estados Unidos
        select2 = (df1['cuisines'] == 'BBQ') & (df1['country'] == 'USA')
        eua_bbq = df1.loc[select2,:]

        #Contar a média de valor do prato para 2 deste grupo
        dfr8_EUA_churrasco = eua_bbq['average_cost_for_two'].mean()

        resultado = [['Comida Japonesa','{:.2f}'.format(dfr8_EUA_comida_japonesa)],['Churrasco BBQ','{:.2f}'.format(dfr8_EUA_churrasco)]]

        dfr8 = pd.DataFrame(resultado, columns=['tipo_restaurante','cozinha'])

        fig = px.pie(dfr8, values='cozinha', names='tipo_restaurante', title='Comparativo de Preço Nos USA Entre Comida Japonesa e BBQ')
        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------
# VISÃO COZINHAS
# --------------------------------------------------------------
with tab4: 
    st.title(':orange[Visão das Cozinhas]')
    
    with st.container():
        st.subheader(f'TOP {qtd} - Maior Valor Médio do Prato Para 2 Pessoas')
                     
        dfr11 = (df1.loc[:,['restaurant_name', 'cuisines', 'country','average_cost_for_two']]
                    .groupby(['restaurant_name', 'cuisines', 'country'])
                    .median()
                    .sort_values('average_cost_for_two', ascending=False)
                    .head(qtd)
                    .reset_index())

        dfr11 = dfr11.rename(columns={'restaurant_name' : 'Nome Restaurante',
                              'cuisines' : 'Cozinhas','country' : 'País',
                              'average_cost_for_two' : 'Valor Médio Para Dois'})
        st.dataframe(dfr11, use_container_width=True)

    with st.container():
        st.subheader(f'TOP {qtd} - Maior Nota de Avaliação Média')

        dfr12 = (df1.loc[:,['restaurant_name', 'cuisines', 'country','aggregate_rating']]
                  .groupby(['restaurant_name', 'cuisines', 'country'])
                  .median()
                  .sort_values('aggregate_rating', ascending=False)
                  .head(qtd)
                  .reset_index())

        dfr12 = dfr12.rename(columns={'restaurant_name' : 'Nome Restaurante',
                                          'cuisines' : 'Cozinhas','country' : 'País',
                                          'aggregate_rating' : 'Avaliação Média'})
        st.dataframe(dfr12, use_container_width=True)

    with st.container():
        st.subheader(f'TOP {qtd} - Culinárias, Cujos Restaurantes Aceitam Pedidos On-Line e Fazem Entregas')

        #Seleciona os restaurantes que aceitam pedidos online e fazem entrega
        select_comida = (df1['has_online_delivery'] == 1) & (df1['is_delivering_now'] == 1)
        df_aux13 = df1.loc[select_comida,:]

        dfr13 = (df_aux13.loc[:,['restaurant_id','cuisines']].groupby(['cuisines'])
                                                            .count()
                                                            .sort_values('restaurant_id', ascending=False)
                                                            .head(qtd)
                                                            .reset_index())

        dfr13 = dfr13.rename(columns={'restaurant_id' : 'Quantidade de Restaurantes',
                                    'cuisines' : 'Tipos de Culinária',})
        st.dataframe(dfr13, use_container_width=True)
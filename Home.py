import streamlit as st
from PIL import Image


#Setar as paginas
st.set_page_config(page_title='Home')

#image_path = 'logo.jpg'
image = Image.open(logo.jpg)
st.sidebar.image(image, width=250)

st.sidebar.header(
    ':orange[FOME ZERO - Um restaurante para cada tipo de fome.]', divider='orange')

st.header(':orange[FOME ZERO!]')
st.subheader(
    ':orange[Um restaurante para cada tipo de fome!]', divider='orange')

st.markdown(
    '''
    ### Dasboard foi elaborado para elucidar os questionamentos feitos pelo CEO da empresa.
    
    ### Como utilizar este Dashboard?
        
    - Na página "Visão Geral" temos a noção do tamanho da empresa nos dias atuais, por meio 
    dos números de paises, cidadades e restaurantes atendidos.
    
    - Na página "Análises" temos as analises em categorias, que são um compilado das principais perguntas do CEO:
        - Países - Analise quantitativa de restaurantes, avaliações e preço do prato para duas pessoas;
            
        - Cidades - Analise que demonstra como estão distribuídos os restaurantes conforme a avalição e
          o tipo de comida servida.
            
        - Restaurantes - Analise dos restaurantes melhor avaliados, mais votados e compartivo de valor
          por tipo de cozinha e por serviço prestado.
            
        - Cozinhas - Analise de valor médio do prato para duas pessoas, melhor avaliação e quantidade
          de restaurantes com serviços agregados.

    ### Dúvidas
    - Consultar Time de Ciência de Dados 
       - @fabioandrade       
    ''')
import streamlit as st
from PIL import Image


#Setar as paginas
st.set_page_config(page_title='Home')

#image_path = 'logo.jpg'
image = Image.open('logo.jpg')
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
        
    - Na "Visão Geral" é possível identificar o crescimento da empresa, por meio dos números de paises, 
    cidades e restaurantes atendidos.
    
    - Em "Análises", dividido em categorias, temos um compilado das principais das respostas as perguntad feitas
    ao time de dados:
    
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

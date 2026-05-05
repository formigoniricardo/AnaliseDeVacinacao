import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard Vacinal ES", layout="wide")

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv('dados_vacinacao_es.csv', sep=';', decimal=',')
        
        df['ano'] = df['ano'].astype(str).str.strip() 
        df['vacina'] = df['vacina'].astype(str).str.strip().str.upper() 
        
        df = df[df['ano'].isin(['2021', '2022'])]
        df = df[df['vacina'].isin(['BCG', 'POLIOMIELITE'])]
        
        df['vacina'] = df['vacina'].replace({'POLIOMIELITE': 'Poliomielite'})
        
        return df
        
    except FileNotFoundError:
        st.error("⚠️ Arquivo 'dados_vacinacao_es.csv' não encontrado na pasta.")
        st.info("Por favor, rode o arquivo 'etl.py' no terminal para gerar a base de dados real antes de iniciar o dashboard.")
        st.stop() 

df_vacina = carregar_dados()

if df_vacina.empty:
    st.error("⚠️ O arquivo CSV foi lido, mas nenhum dado válido foi encontrado. Verifique se o ETL foi executado.")
    st.stop()

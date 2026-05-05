import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard Vacinal ES", layout="wide")

@st.cache_data
def carregar_dados_prototipo():
    cidades_es = {
        'Vitória': [-20.3155, -40.3128],
        'Vila Velha': [-20.3297, -40.2925],
        'Serra': [-20.1286, -40.3078],
        'Cariacica': [-20.2638, -40.4200],
        'Linhares': [-19.3911, -40.0722],
        'Colatina': [-19.5314, -40.6316],
        'Guarapari': [-20.6667, -40.4950],
        'São Mateus': [-18.7161, -39.8589],
        'Cachoeiro de Itapemirim': [-20.8489, -41.1128],
        'Aracruz': [-19.8202, -40.2733]
    }
    
    vacinas = ['BCG', 'Poliomielite', 'Pentavalente']
    anos = [2021, 2022, 2023]
    
    dados = []
    for ano in anos:
        for mun, coords in cidades_es.items():
            for vac in vacinas:
                cobertura = np.random.uniform(70.0, 99.0)
                dados.append([ano, 'ES', mun, vac, cobertura, coords[0], coords[1]])
                
    return pd.DataFrame(dados, columns=['ano', 'sigla_uf', 'municipio', 'vacina', 'cobertura_vacinal', 'lat', 'lon'])

df_vacina = carregar_dados_prototipo()

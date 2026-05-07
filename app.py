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

st.sidebar.title("Filtros de Análise")
ano_selecionado = st.sidebar.selectbox(
    "Selecione o Ano:", sorted(df_vacina['ano'].unique(), reverse=True))
vacina_selecionada = st.sidebar.selectbox(
    "Selecione a Vacina:", df_vacina['vacina'].unique())

df_filtrado = df_vacina[(df_vacina['ano'] == ano_selecionado) & (
    df_vacina['vacina'] == vacina_selecionada)].copy()
df_filtrado['cobertura_vacinal'] = pd.to_numeric(
    df_filtrado['cobertura_vacinal'], errors='coerce').round(2)
df_filtrado['status'] = np.where(
    df_filtrado['cobertura_vacinal'] >= 95, 'Alcançada', 'Abaixo da Meta')

st.title("Dashboard de Cobertura Vacinal - Espírito Santo")
st.info("Objetivo: Monitorar os municípios e identificar hiatos imunológicos. A meta de segurança estipulada pelo Ministério da Saúde é de 95% de cobertura para evitar o retorno de doenças erradicadas.")
st.warning("⚠️ *Aviso Importante:* Os cálculos de porcentagem apresentados neste painel são médias aproximadas baseadas em estimativas populacionais para fins acadêmicos. Estes dados não são oficiais e podem conter erros ou imprecisões.")

col1, col2, col3 = st.columns(3)
media_atual = df_filtrado['cobertura_vacinal'].mean()
municipios_risco = len(df_filtrado[df_filtrado['cobertura_vacinal'] < 95])
total_municipios = len(df_filtrado)

col1.metric(label=f"Média Estadual ({ano_selecionado})",
            value=f"{media_atual:.2f}%", delta=f"{media_atual - 95:.2f}% em relação à meta")
col2.metric(label="Meta do Ministério da Saúde", value="95.00%")
col3.metric(label="Municípios em Risco (< 95%)",
            value=f"{municipios_risco} de {total_municipios}")

st.markdown("---")

col_mapa, col_grafico = st.columns([1.5, 1])

with col_mapa:
    st.subheader(
        f"Mapa Interativo: Cobertura {vacina_selecionada} ({ano_selecionado})")

    fig_mapa = px.scatter_mapbox(
        df_filtrado,
        lat="lat",
        lon="lon",
        color="cobertura_vacinal",
        size="cobertura_vacinal",
        hover_name="municipio",
        hover_data={"lat": False, "lon": False,
                    "cobertura_vacinal": True, "status": True},
        color_continuous_scale=px.colors.diverging.RdYlGn,
        range_color=[60, 100],
        zoom=6.5,
        center={"lat": -19.6, "lon": -40.3},
        mapbox_style="carto-positron",
        labels={'cobertura_vacinal': 'Cobertura (%)', 'status': 'Situação'},
        opacity=0.85,
        size_max=14
    )

    fig_mapa.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig_mapa, use_container_width=True)

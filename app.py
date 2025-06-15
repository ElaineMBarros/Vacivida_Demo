
import streamlit as st
import pandas as pd

@st.cache_data
def load_dose_data():
    return pd.read_csv("prod.vcvd_dose.csv", sep=";", encoding="ISO-8859-1")

df_dose = load_dose_data()

st.set_page_config(layout="wide")
st.title("Vacivida - Análise de Vacinação")

tabs = st.tabs(["📋 Dados de Vacinação"])

with tabs[0]:
    st.subheader("📊 Filtros")
    col1, col2 = st.columns(2)
    with col1:
        vacinas = df_dose["vcvd_nome_vacina"].dropna().unique() if "vcvd_nome_vacina" in df_dose else []
        vacina = st.selectbox("Filtrar por Nome da Vacina", options=vacinas)
    with col2:
        datas = pd.to_datetime(df_dose["createdon"], errors='coerce') if "createdon" in df_dose else []
        data_inicial = st.date_input("Data inicial", value=datas.min().date() if not datas.empty else None)
        data_final = st.date_input("Data final", value=datas.max().date() if not datas.empty else None)

    # Aplicar filtro
    df_filtrado = df_dose.copy()
    if vacina:
        df_filtrado = df_filtrado[df_filtrado["vcvd_nome_vacina"] == vacina]
    if not datas.empty:
        df_filtrado["createdon"] = pd.to_datetime(df_filtrado["createdon"], errors='coerce')
        df_filtrado = df_filtrado[
            (df_filtrado["createdon"].dt.date >= data_inicial) &
            (df_filtrado["createdon"].dt.date <= data_final)
        ]

    st.dataframe(df_filtrado)

    # Exportação
    st.download_button(
        label="📥 Exportar para Excel",
        data=df_filtrado.to_excel(index=False, engine="openpyxl"),
        file_name="dados_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

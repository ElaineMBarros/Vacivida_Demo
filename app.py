
import streamlit as st
import pandas as pd
from io import BytesIO

@st.cache_data
def load_data():
    df = pd.read_csv("prod.vcvd_dose.csv", encoding="latin1", sep=";")
    return df

def gerar_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Vacinação")
    output.seek(0)
    return output

def main():
    st.set_page_config(page_title="Vacivida - Análise de Vacinação", layout="wide")
    st.title("📊 Vacivida - Análise de Vacinação e Desfecho")

    df = load_data()

    st.sidebar.header("Filtros")

    vacinas = df["NomeVacina"].dropna().unique().tolist()
    vacina = st.sidebar.selectbox("Nome da Vacina", options=["Todas"] + vacinas)

    status = df["StatusCaso"].dropna().unique().tolist()
    status_filtro = st.sidebar.multiselect("Status do Paciente", options=status, default=status)

    if vacina != "Todas":
        df = df[df["NomeVacina"] == vacina]

    if status_filtro:
        df = df[df["StatusCaso"].isin(status_filtro)]

    st.markdown(f"### Resultados: {len(df)} registros encontrados")
    st.dataframe(df)

    excel_data = gerar_excel(df)
    st.download_button(label="📥 Baixar Excel", data=excel_data, file_name="dados_vacinados.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()

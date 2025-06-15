
import streamlit as st
import pandas as pd

@st.cache_data
def load_dfs():
    kwargs = {
        'encoding': 'latin1',
        'sep': ',',
        'engine': 'python',
        'on_bad_lines': 'skip'
    }
    df_dose = pd.read_csv("prod.vcvd_dose.csv", **kwargs)
    df_bio = pd.read_csv("prod.vcvd_bioquimica.csv", **kwargs)
    df_hem = pd.read_csv("prod.vcvd_hemograma.csv", **kwargs)
    return df_dose, df_bio, df_hem

def main():
    st.title("Vacivida Dashboard")
    df_dose, df_bio, df_hem = load_dfs()

    st.sidebar.header("Filtros")
    paciente_id = st.sidebar.text_input("Paciente ID")
    vacina = st.sidebar.selectbox("Nome da Vacina", options=df_dose['NomeVacina'].dropna().unique())
    status = st.sidebar.selectbox("Status do Caso", options=df_dose['StatusCaso'].dropna().unique())

    st.subheader("Dados de Doses")
    df_filtered = df_dose[
        (df_dose['NomeVacina'] == vacina) &
        (df_dose['StatusCaso'] == status)
    ]
    if paciente_id:
        df_filtered = df_filtered[df_filtered['PacienteId'].astype(str) == paciente_id]

    st.dataframe(df_filtered)

    st.download_button(
        label="📥 Exportar para Excel",
        data=df_filtered.to_csv(index=False).encode('utf-8'),
        file_name='dados_filtrados.csv',
        mime='text/csv'
    )

    st.subheader("Dados Bioquímicos")
    st.dataframe(df_bio)

    st.subheader("Hemograma")
    st.dataframe(df_hem)

if __name__ == "__main__":
    main()

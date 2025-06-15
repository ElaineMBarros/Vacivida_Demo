import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config("Dashboard Vacinação & Exames", layout="wide")

@st.cache_data
def load_dfs():
    df_dose = pd.read_csv("prod.vcvd_dose.csv")
    df_bio = pd.read_csv("prod.vcvd_bioquimica.csv")
    df_hem = pd.read_csv("prod.vcvd_hemograma.csv")
    return df_dose, df_bio, df_hem

df_dose, df_bio, df_hem = load_dfs()

tab1, tab2, tab3 = st.tabs(["Vacinação", "Exames", "Exportar PDF/Excel"])

with tab1:
    st.header("📈 Vacinação & Reações")
    vacinas = sorted(df_dose["vcvd_nome_vacina"].dropna().unique())
    sel = st.multiselect("Vacina", vacinas, default=vacinas)
    adversa = st.checkbox("Filtrar reações adversas?")
    df_vac = df_dose[df_dose["vcvd_nome_vacina"].isin(sel)]
    if adversa:
        df_vac = df_vac[df_vac["vcvd_tipo_manifestacao"]=="Adversa"]
    vacinados = df_vac["vcvd_paciente_id"].nunique()
    reacoes = df_vac[df_vac["vcvd_tipo_manifestacao"]=="Adversa"]["vcvd_paciente_id"].nunique() if adversa else 0
    pct = f"{reacoes/vacinados*100:.1f}%" if vacinados else "0%"
    c1, c2, c3 = st.columns(3)
    c1.metric("Pacientes", vacinados)
    c2.metric("Reações", reacoes)
    c3.metric("% Reações", pct)
    fig = px.bar(
        df_vac.groupby("vcvd_nome_vacina")["vcvd_paciente_id"].nunique().reset_index(name="Total"),
        x="vcvd_nome_vacina", y="Total",
        title="Total de vacinados por vacina"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_vac[["vcvd_paciente_id","vcvd_nome_vacina","vcvd_tipo_manifestacao"]].drop_duplicates())

with tab2:
    st.header("🔬 Exames Clínicos")
    exame = st.selectbox("Tipo de exame", ["Creatinina","TGP","TGO"])
    df_src = df_bio if exame in ["Creatinina","TGP","TGO"] else df_hem
    col = {
        "Creatinina": "vcvd_creatinina_mgdl",
        "TGP": "vcvd_alt_tgp",
        "TGO": "vcvd_ast_tgo"
    }[exame]
    df_exame = df_src[["vcvd_paciente_id", col, "vcvd_data_coleta"]].dropna()
    st.dataframe(df_exame)
    fig2 = px.line(
        df_exame, x="vcvd_data_coleta", y=col, color="vcvd_paciente_id",
        title=f"{exame} ao longo do tempo"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("📄 Exportar PDF e Excel")
    fig = px.line(
        df_bio.sort_values("vcvd_data_coleta"),
        x="vcvd_data_coleta", y="vcvd_creatinina_mgdl",
        title="Creatinina ao longo do tempo"
    )
    st.plotly_chart(fig, use_container_width=True)

    buf_pdf = BytesIO()
    fig.write_image(buf_pdf, format="pdf")
    buf_pdf.seek(0)
    st.download_button("⬇️ Baixar PDF", buf_pdf, "grafico_creatinina.pdf", "application/pdf")

    buf_xlsx = BytesIO()
    with pd.ExcelWriter(buf_xlsx, engine="xlsxwriter") as writer:
        df_vac.to_excel(writer, sheet_name="Vacinação", index=False)
        df_exame.to_excel(writer, sheet_name=exame, index=False)
        writer.save()
    buf_xlsx.seek(0)
    st.download_button(
        label="⬇️ Baixar Excel (Vacinados + Exame)",
        data=buf_xlsx.getvalue(),
        file_name="relatorio_vacina_exame.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

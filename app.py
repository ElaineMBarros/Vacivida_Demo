import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
import plotly.express as px
from utils import *
from config import *

# Configuração da página
st.set_page_config(
    page_title=APP_NAME,
    layout=STREAMLIT_CONFIG['layout'],
    initial_sidebar_state=STREAMLIT_CONFIG['initial_sidebar_state']
)

# Cache de dados
@st.cache_data(ttl=CACHE_CONFIG['ttl'], max_entries=CACHE_CONFIG['max_entries'])
def load_data():
    df = pd.read_csv("prod.vcvd_dose.csv", encoding="latin1", sep=";")
    df = process_date_columns(df)
    df = calculate_age(df)
    df = create_temporal_features(df)
    return df

def main():
    # Título e descrição
    st.title(f"📊 {APP_NAME}")
    st.markdown(f"""
    ### {APP_DESCRIPTION}
    Versão {APP_VERSION}
    
    Este dashboard oferece uma visão completa dos dados de vacinação, incluindo análises estatísticas,
    tendências temporais e insights sobre a cobertura vacinal.
    """)

    # Carregamento dos dados
    df = load_data()

    # Sidebar com filtros avançados
    st.sidebar.header("🔍 Filtros Avançados")
    
    # Filtro de período
    if 'DataVacinacao' in df.columns:
        min_date = df['DataVacinacao'].min()
        max_date = df['DataVacinacao'].max()
        date_range = st.sidebar.date_input(
            "📅 Período de Análise",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    # Filtro de vacinas
    vacinas = df["NomeVacina"].dropna().unique().tolist()
    vacina = st.sidebar.selectbox(
        "💉 Tipo de Vacina",
        options=["Todas"] + sorted(vacinas)
    )

    # Filtro de status
    status = df["StatusCaso"].dropna().unique().tolist()
    status_filtro = st.sidebar.multiselect(
        " Status do Paciente",
        options=sorted(status),
        default=status
    )

    # Filtro de idade
    if 'Idade' in df.columns:
        idade_min, idade_max = st.sidebar.slider(
            "👥 Faixa Etária",
            min_value=int(df['Idade'].min()),
            max_value=int(df['Idade'].max()),
            value=(int(df['Idade'].min()), int(df['Idade'].max()))
        )

    # Aplicação dos filtros
    if vacina != "Todas":
        df = df[df["NomeVacina"] == vacina]

    if status_filtro:
        df = df[df["StatusCaso"].isin(status_filtro)]

    if 'DataVacinacao' in df.columns and len(date_range) == 2:
        df = df[(df['DataVacinacao'].dt.date >= date_range[0]) & 
                (df['DataVacinacao'].dt.date <= date_range[1])]

    if 'Idade' in df.columns:
        df = df[(df['Idade'] >= idade_min) & (df['Idade'] <= idade_max)]

    # Métricas principais
    st.markdown("### 📈 Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Registros",
            len(df),
            f"{len(df) - len(df[df['DataVacinacao'].dt.date >= (datetime.now() - timedelta(days=30)).date()])} nos últimos 30 dias"
        )
    
    with col2:
        st.metric(
            "Total de Vacinas Únicas",
            df["NomeVacina"].nunique()
        )
    
    with col3:
        st.metric(
            "Status Mais Comum",
            df["StatusCaso"].mode().iloc[0],
            f"{df['StatusCaso'].value_counts().iloc[0]} casos"
        )
    
    with col4:
        if 'Idade' in df.columns:
            st.metric(
                "Idade Média",
                f"{df['Idade'].mean():.1f} anos",
                f"±{df['Idade'].std():.1f} anos"
            )

    # Análise Temporal
    st.markdown("### 📅 Análise Temporal")
    temporal_plot = create_temporal_plot(df)
    if temporal_plot:
        st.plotly_chart(temporal_plot, use_container_width=True)

    # Análise Demográfica
    st.markdown("### 👥 Análise Demográfica")
    if 'Idade' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            age_dist = create_age_distribution(df)
            if age_dist:
                st.plotly_chart(age_dist, use_container_width=True)
        
        with col2:
            stats_df = get_statistical_analysis(df, 'Idade')
            if stats_df is not None:
                st.markdown("#### Estatísticas de Idade")
                st.dataframe(stats_df, use_container_width=True)

    # Análise de Status e Vacinas
    st.markdown("### 💉 Análise de Status e Vacinas")
    col1, col2 = st.columns(2)
    
    with col1:
        status_dist = create_status_distribution(df)
        if status_dist:
            st.plotly_chart(status_dist, use_container_width=True)
    
    with col2:
        vaccine_dist = create_vaccine_distribution(df)
        if vaccine_dist:
            st.plotly_chart(vaccine_dist, use_container_width=True)

    # Tabela de dados
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

    # Botões de download
    col1, col2 = st.columns(2)
    
    with col1:
        excel_data = BytesIO()
        with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=EXPORT_CONFIG['excel']['sheet_name'], index=EXPORT_CONFIG['excel']['index'])
            
            # Adicionar sumário estatístico
            if 'Idade' in df.columns:
                stats_df = get_statistical_analysis(df, 'Idade')
                if stats_df is not None:
                    stats_df.to_excel(writer, sheet_name="Sumário")
        
        excel_data.seek(0)
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_data,
            file_name="dados_vacinados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        st.download_button(
            label="📄 Baixar Relatório PDF",
            data="Relatório em PDF",  # Implementar geração de PDF
            file_name="relatorio_vacinacao.pdf",
            mime="application/pdf"
        )

    # Rodapé
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center'>
        <p>Desenvolvido com ❤️ pela equipe Vacivida</p>
        <p>Última atualização: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

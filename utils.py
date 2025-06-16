import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

def process_date_columns(df):
    """Processa colunas de data no DataFrame"""
    date_columns = [col for col in df.columns if 'Data' in col]
    for col in date_columns:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        except:
            continue
    return df

def calculate_age(df):
    """Calcula idade baseado na data de nascimento"""
    if 'DataNascimento' in df.columns:
        df['Idade'] = ((datetime.now() - df['DataNascimento']).dt.days / 365.25).round(1)
    return df

def create_temporal_features(df):
    """Cria features temporais"""
    if 'DataVacinacao' in df.columns:
        df['MesAno'] = df['DataVacinacao'].dt.strftime('%Y-%m')
        df['DiaSemana'] = df['DataVacinacao'].dt.day_name()
        df['DiaMes'] = df['DataVacinacao'].dt.day
        df['Mes'] = df['DataVacinacao'].dt.month
        df['Ano'] = df['DataVacinacao'].dt.year
    return df

def get_statistical_analysis(df, column):
    """Retorna análise estatística de uma coluna"""
    if column in df.columns:
        stats_dict = {
            'count': len(df),
            'mean': df[column].mean(),
            'std': df[column].std(),
            'min': df[column].min(),
            '25%': df[column].quantile(0.25),
            '50%': df[column].quantile(0.50),
            '75%': df[column].quantile(0.75),
            'max': df[column].max()
        }
        return pd.DataFrame.from_dict(stats_dict, orient='index', columns=['Valor'])
    return None

def create_temporal_plot(df):
    """Cria gráfico temporal"""
    if 'MesAno' in df.columns:
        df_temporal = df.groupby('MesAno').size().reset_index(name='count')
        fig = px.line(
            df_temporal,
            x='MesAno',
            y='count',
            title='Evolução Temporal das Vacinações',
            labels={'MesAno': 'Mês', 'count': 'Número de Vacinações'}
        )
        return fig
    return None

def create_age_distribution(df):
    """Cria distribuição de idade"""
    if 'Idade' in df.columns:
        fig = px.histogram(
            df,
            x='Idade',
            nbins=30,
            title='Distribuição por Idade',
            labels={'Idade': 'Idade (anos)', 'count': 'Frequência'}
        )
        return fig
    return None

def create_status_distribution(df):
    """Cria distribuição de status"""
    if 'StatusCaso' in df.columns:
        fig = px.pie(
            df,
            names="StatusCaso",
            title="Distribuição por Status"
        )
        return fig
    return None

def create_vaccine_distribution(df):
    """Cria distribuição de vacinas"""
    if 'NomeVacina' in df.columns:
        fig = px.bar(
            df["NomeVacina"].value_counts().reset_index(),
            x="index",
            y="NomeVacina",
            title="Distribuição por Tipo de Vacina",
            labels={"index": "Vacina", "NomeVacina": "Quantidade"}
        )
        return fig
    return None 
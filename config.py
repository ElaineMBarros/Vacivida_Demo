import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações da aplicação
APP_NAME = os.getenv('APP_NAME', 'Vacivida Dashboard')
APP_DESCRIPTION = os.getenv('APP_DESCRIPTION', 'Dashboard de Análise de Vacinação')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
DATA_DIR = os.getenv('DATA_DIR', './data')

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    'theme': {
        'primaryColor': '#1E88E5',
        'backgroundColor': '#FFFFFF',
        'secondaryBackgroundColor': '#F0F2F6',
        'textColor': '#262730',
        'font': 'sans serif'
    },
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Configurações de cache
CACHE_CONFIG = {
    'ttl': 3600,  # 1 hora
    'max_entries': 100
}

# Configurações de exportação
EXPORT_CONFIG = {
    'excel': {
        'sheet_name': 'Dados Completos',
        'index': False
    },
    'pdf': {
        'page_size': 'A4',
        'orientation': 'portrait'
    }
} 
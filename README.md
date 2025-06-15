
# Vacivida - Dashboard de Vacinação

Este projeto é um painel em Streamlit que analisa dados de vacinação da COVID-19 e status de pacientes com base nos registros da base pública `prod.vcvd_dose.csv`.

## Funcionalidades

- Filtros por Nome da Vacina e Status do Paciente
- Tabela interativa dos registros
- Exportação dos resultados em Excel

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Requisitos

- Python 3.8+
- Streamlit
- pandas
- openpyxl

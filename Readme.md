# Dashboard Vacinação & Exames

Este repositório contém um app em Streamlit para análises clínicas, visualizações interativas e exportação de relatórios.

## Funcionalidades

- **Aba "Vacinação"**: filtros por vacina e reações adversas, gráficos e tabela.
- **Aba "Exames"**: visualização dos exames clínicos escolhidos.
- **Aba "Exportar PDF/Excel"**:
  - Gera e faz download de gráfico (PDF).
  - Exporta dados de vacinação e exames em planilha Excel com múltiplas abas.

## Instalação e execução

```bash
pip install -r requirements.txt
streamlit run app.py

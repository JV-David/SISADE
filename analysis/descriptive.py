import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from components.metrics import metric_card, analysis_card
from utils.plotting import plot_correlation_matrix, plot_distribution

def perform_descriptive_analysis(df):
    """Realiza análise estatística descritiva"""
    results = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_card("📋 Informações Gerais", f"""
        - **Linhas:** {df.shape[0]:,}
        - **Colunas:** {df.shape[1]:,}
        - **Valores ausentes:** {df.isnull().sum().sum():,}
        - **Duplicatas:** {df.duplicated().sum():,}
        """)
        
        # Mostrar tipos de dados
        dtype_counts = df.dtypes.value_counts()
        type_info = "\n".join([f"- **{dtype}:** {count} colunas" for dtype, count in dtype_counts.items()])
        analysis_card("📌 Tipos de Dados", type_info)
    
    with col2:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            #analysis_card("🧮 Estatísticas Numéricas", df[numeric_cols].describe().style.format("{:.2f}").to_html(), is_html=True)
            analysis_card("🧮 Estatísticas Numéricas", df[numeric_cols].describe().style.format("{:.2f}").to_html())
        else:
            st.warning("Nenhuma coluna numérica encontrada.")
    
    # Análise de valores ausentes
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]
    
    if len(missing_data) > 0:
        plot_missing_values(missing_data)
    else:
        st.success("✅ Nenhum valor ausente encontrado.")
    
    # Gráficos de distribuição
    if len(numeric_cols) > 0:
        selected_num_col = st.selectbox("Selecione uma variável numérica:", numeric_cols)
        plot_distribution(df, selected_num_col)
    
    # Análise de correlação
    if len(numeric_cols) > 1:
        plot_correlation_matrix(df[numeric_cols])
    
    results.update({
        'shape': df.shape,
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum(),
        'numeric_columns': len(numeric_cols),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns)
    })
    
    return results

def plot_missing_values(missing_data):
    """Plota gráfico de valores ausentes"""
    fig = px.bar(missing_data, 
                x=missing_data.index, 
                y=missing_data.values,
                labels={'x': 'Variável', 'y': 'Valores Ausentes'},
                title='Valores Ausentes por Variável')
    st.plotly_chart(fig, use_container_width=True)
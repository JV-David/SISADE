import streamlit as st
import pandas as pd
import numpy as np
import config
from core.data_processor import clean_data

def render_sidebar():

    st.markdown("""
    <style>
        .hideScrollbar .st-emotion-cache-79elbk {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.header("📁 Carregar Dados")
    
    # Opção de dados de exemplo
    if st.sidebar.button("🔬 Usar Dados de Exemplo (Epidemiológicos)", key="sample_data"):
        np.random.seed(42)
        n_samples = config.DEFAULT_SAMPLE_SIZE
        
        df = pd.DataFrame({
            'idade': np.random.normal(65, 15, n_samples).astype(int),
            'sexo': np.random.choice(['Masculino', 'Feminino'], n_samples),
            'hipertensao': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            'diabetes': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'tabagismo': np.random.choice(['Não', 'Sim'], n_samples, p=[0.8, 0.2]),
            'tratamento': np.random.choice(['A', 'B', 'C'], n_samples, p=[0.5, 0.3, 0.2]),
            'tempo_internacao': np.random.exponential(7, n_samples).round(1),
            'tempo_sobrevivencia': np.random.weibull(1.5, n_samples) * 100,
            'status_obito': np.random.choice([1, 0], n_samples, p=[0.3, 0.7]),
            'custo_tratamento': np.random.normal(5000, 2000, n_samples).round(2),
            'comorbidades': np.random.randint(0, 4, n_samples)
        })
        
        # Ajustes para tornar os dados mais realistas
        df['idade'] = df['idade'].clip(18, 95)
        df['tempo_internacao'] = df['tempo_internacao'].clip(1, 30)
        df['tempo_sobrevivencia'] = df['tempo_sobrevivencia'].clip(1, 365)
        df['custo_tratamento'] = df['custo_tratamento'].clip(1000, 15000)
        
        # Adicionar alguns valores ausentes
        for col in np.random.choice(df.columns, 3):
            df.loc[df.sample(frac=0.1).index, col] = np.nan
        
        st.session_state.df = clean_data(df)
        st.success("Dados de exemplo carregados com sucesso!")
    
    # Upload de arquivo
    uploaded_file = st.sidebar.file_uploader(
        "Escolha um arquivo CSV ou Excel",
        type=['csv', 'xlsx', 'xls'],
        key="file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            if df.empty:
                st.error("O arquivo carregado está vazio.")
            else:
                st.session_state.df = clean_data(df)
                st.success("Dados carregados com sucesso!")
        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {str(e)}")
    
    # Configuração da API
    st.sidebar.header("🔑 Configuração")
    st.session_state.api_key = st.sidebar.text_input(
        "API Key do Gemini:", 
        type="password",
        help="Obtenha sua chave em https://makersuite.google.com/app/apikey",
        key="api_key_input"
    )
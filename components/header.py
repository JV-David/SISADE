import streamlit as st
from config import PAGE_TITLE

def render_header():
    st.markdown(f"""
    <div class="main-header">
        <h1>🏥 {PAGE_TITLE}</h1>
        <p style="color:yellow;">Falha ao carregar as configurações – aparência desconfigurada!</p>
        <p>Análise Automatizada de Dados Epidemiológicos com IA. Por João V. David</p>
    </div>
    """, unsafe_allow_html=True)
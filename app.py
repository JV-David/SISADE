import streamlit as st
from components.header import render_header
from components.footer import show_footer
from components.sidebar import render_sidebar
from pages.home import render_home
from pages.descriptive import render_descriptive
from pages.survival import render_survival
from pages.predictive import render_predictive
from pages.report import render_report
import config
from styles import load_css

def main():
    # Configuração da página
    st.set_page_config(
        page_title=config.PAGE_TITLE,
        page_icon=config.PAGE_ICON,
        layout=config.PAGE_LAYOUT,
        initial_sidebar_state=config.SIDEBAR_STATE
    )
    
    # Carregar CSS personalizado
    load_css()
    
    # Renderizar cabeçalho
    render_header()
    
    # Inicializar estado da sessão
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    # Renderizar sidebar e obter dados
    render_sidebar()
    
    # Navegação entre páginas
    page = st.sidebar.radio(
        "Navegação",
        options=["🏠 Início", "📈 Descritiva", "⏳ Sobrevivência", "🤖 Preditiva", "📄 Relatório"],
        key="page_navigation"
    )
    
    # Renderizar página selecionada
    if page == "🏠 Início":
        render_home()
    elif page == "📈 Descritiva" and st.session_state.df is not None:
        render_descriptive()
    elif page == "⏳ Sobrevivência" and st.session_state.df is not None:
        render_survival()
    elif page == "🤖 Preditiva" and st.session_state.df is not None:
        render_predictive()
    elif page == "📄 Relatório" and st.session_state.df is not None:
        render_report()
    elif st.session_state.df is None:
        st.warning("Por favor, carregue dados primeiro na página inicial")

    show_footer()
if __name__ == "__main__":
    main()
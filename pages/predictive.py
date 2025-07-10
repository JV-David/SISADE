import streamlit as st
from analysis.predictive import perform_predictive_analysis
from core.analyzer import SISADEAnalyzer

def render_predictive():
    """Renderiza a página de análise preditiva"""
    if 'data_info' in st.session_state.analysis_results:
        target_options = (
            st.session_state.analysis_results['data_info']['target_variables']
            if isinstance(st.session_state.analysis_results['data_info']['target_variables'], list)
            else list(st.session_state.analysis_results['data_info']['target_variables'].keys())
        )
        
        if len(target_options) > 0:
            target_col = st.selectbox(
                "Escolha a variável alvo:",
                target_options,
                key="target_select"
            )
            
            if st.button("🚀 Executar Análise Preditiva", key="run_predictive"):
                with st.spinner("Treinando modelo..."):
                    pred_results = perform_predictive_analysis(st.session_state.df, target_col)
                    st.session_state.analysis_results['predictive'] = pred_results
                
                # Interpretação dos resultados preditivos
                if st.session_state.api_key and pred_results:
                    analyzer = SISADEAnalyzer(st.session_state.api_key)
                    with st.spinner("🤖 Interpretando resultados preditivos..."):
                        interpretation = analyzer.interpret_results(pred_results, "Análise Preditiva")
                        st.markdown("### 💡 Interpretação IA")
                        st.markdown(interpretation)
        else:
            st.warning("Nenhuma variável alvo identificada automaticamente.")
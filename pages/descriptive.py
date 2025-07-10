import streamlit as st
from analysis.descriptive import perform_descriptive_analysis
from core.analyzer import SISADEAnalyzer

def render_descriptive():
    """Renderiza a página de análise descritiva com formatação melhorada"""
    st.subheader("📈 Análise Estatística Descritiva")
    
    if st.session_state.df is not None:
        desc_results = perform_descriptive_analysis(st.session_state.df)
        st.session_state.analysis_results['descriptive'] = desc_results
        
        if st.session_state.api_key:
            analyzer = SISADEAnalyzer(st.session_state.api_key)
            with st.spinner("🤖 Interpretando resultados descritivos..."):
                interpretation = analyzer.interpret_results(desc_results, "Análise Descritiva")
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: {COLOR_PRIMARY};">💡 Interpretação IA</h3>
                    <div style="padding: 10px; line-height: 1.6;">
                        {interpretation}
                    </div>
                </div>
                """, unsafe_allow_html=True)
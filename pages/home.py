import streamlit as st
from core.analyzer import SISADEAnalyzer
from components.metrics import analysis_card
from config import COLOR_PRIMARY, COLOR_SECONDARY

def render_home():
    """Renderiza a página inicial com formatação melhorada"""
    if st.session_state.df is not None:
        analyzer = SISADEAnalyzer(st.session_state.api_key)
        
        with st.spinner("🤖 Analisando estrutura dos dados com IA..."):
            analysis = analyzer.analyze_data_structure(st.session_state.df)
            st.session_state.analysis_results['data_info'] = analysis
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_vars = "".join([f"<li style='margin-bottom: 5px;'><strong>{var}</strong></li>" 
                                 for var in (analysis['target_variables'][:5] if isinstance(analysis['target_variables'], list) 
                                           else list(analysis['target_variables'].keys())[:5])])
            
            issues = "".join([f"<li style='margin-bottom: 5px;'><strong>{k}:</strong> {v}</li>" 
                            for k, v in analysis['data_issues'].items()])
            
            analysis_content = f"""
            <div style="line-height: 1.6;">
                <p><strong style="color: {COLOR_SECONDARY};">Tipo de dados:</strong> {analysis['data_type']}</p>
                <p><strong style="color: {COLOR_SECONDARY};">Problema identificado:</strong> {analysis['problem_type']}</p>
                
                <p style="margin-top: 15px;"><strong style="color: {COLOR_SECONDARY};">Variáveis-alvo sugeridas:</strong></p>
                <ul style="margin-top: 5px; padding-left: 20px;">
                    {target_vars}
                </ul>
                
                <p style="margin-top: 15px;"><strong style="color: {COLOR_SECONDARY};">Possíveis problemas nos dados:</strong></p>
                <ul style="margin-top: 5px; padding-left: 20px;">
                    {issues}
                </ul>
            </div>
            """
            analysis_card("🎯 Análise Automática", analysis_content)
        
        with col2:
            recommended = "".join([f"<li style='margin-bottom: 8px;'><span style='color: {COLOR_PRIMARY};'>✓</span> {analysis_type}</li>" 
                                 for analysis_type in analysis['recommended_analyses']])
            
            analysis_card("📋 Análises Recomendadas", 
                        f"<ul style='margin-top: 5px; padding-left: 20px;'>{recommended}</ul>")
        
        if 'interpretation' in analysis:
            st.markdown(f"""
            <div class="metric-card" style="margin-top: 20px;">
                <h3 style="color: {COLOR_PRIMARY};">💡 Interpretação IA</h3>
                <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                    {analysis['interpretation']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("👀 Visualizar Dados", expanded=False):
            st.dataframe(st.session_state.df.head(10))
    
    else:
        st.info("👆 Carregue um arquivo de dados ou use os dados de exemplo na barra lateral.")
        
        st.markdown("""
        ### 🎯 Sobre o SISADE
        
        O **Sistema de Inteligência Estatística para Análise de Dados Epidemiológicos** utiliza:
        
        - **🤖 IA Generativa** (Gemini) para identificar automaticamente o tipo de dados
        - **📊 Análises Estatísticas** descritivas e inferenciais
        - **⏳ Análise de Sobrevivência** (Kaplan-Meier, log-rank)
        - **🔮 Machine Learning** para análises preditivas
        - **📈 Visualizações** interativas e informativas
        - **📄 Relatórios** automatizados com interpretações em linguagem clara
        
        ### 🚀 Como usar:
        1. Configure sua API Key do Gemini na barra lateral
        2. Carregue seus dados (CSV/Excel) ou use os dados de exemplo
        3. O sistema identificará automaticamente o tipo de análise mais adequada
        4. Explore os resultados nas diferentes abas
        5. Gere relatórios executivos com interpretações em linguagem acessível
        
        ### 📚 Casos de Uso:
        - Análise de eficácia de tratamentos
        - Predição de riscos e outcomes clínicos
        - Estudos epidemiológicos
        - Análise de custos hospitalares
        - Pesquisa acadêmica em saúde
        """)
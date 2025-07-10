import streamlit as st
from core.report_generator import generate_report

def render_report():
    """Renderiza a página de relatórios com tratamento robusto de erros"""
    
    # Section header
    st.header("📑 Relatório Analítico")
    
    # Check prerequisites before generating report
    if 'analysis_results' not in st.session_state:
        st.warning("⚠️ Nenhum dado analisado encontrado. Por favor, execute as análises primeiro.")
        return
    
    if 'df' not in st.session_state:
        st.error("❌ Dados não carregados. Por favor, importe um dataset primeiro.")
        return
    
    # Report generation button
    if st.button("📊 Gerar Relatório Completo", 
                key="generate_report",
                help="Clique para gerar um relatório detalhado com todas as análises"):
        
        # Add AI interpretation if API key is available
        if st.session_state.get('api_key'):
            try:
                from core.analyzer import SISADEAnalyzer
                with st.spinner("🤖 Gerando interpretação final com IA..."):
                    analyzer = SISADEAnalyzer(st.session_state.api_key)
                    interpretation = analyzer.interpret_results(
                        st.session_state.analysis_results, 
                        "Relatório Executivo Completo"
                    )
                    st.session_state.analysis_results['interpretation'] = interpretation
                    st.success("✅ Interpretação gerada com sucesso!")
            except Exception as e:
                st.error(f"❌ Falha na interpretação por IA: {str(e)}")
                st.session_state.analysis_results['interpretation'] = "Interpretação não disponível"
        
        # Generate and display the report
        try:
            with st.spinner("📝 Compilando relatório..."):
                report = generate_report(st.session_state.analysis_results, st.session_state.df)
                
                # Display report in expandable sections
                with st.expander("🔍 Visualizar Relatório Completo", expanded=True):
                    st.markdown(report, unsafe_allow_html=True)
                
                # Add download option
                st.download_button(
                    label="⬇️ Download do Relatório (HTML)",
                    data=report,
                    file_name="relatorio_analitico.html",
                    mime="text/html"
                )
                
        except KeyError as e:
            st.error(f"🔑 Dados incompletos para gerar relatório: {str(e)}")
        except Exception as e:
            st.error(f"❌ Erro inesperado ao gerar relatório: {str(e)}")
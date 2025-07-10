from datetime import datetime
import base64
import streamlit as st

def generate_report(analysis_results, df):
    """Gera um relatório completo"""
    st.subheader("📄 Relatório Executivo")
    
    # Cabeçalho do relatório
    st.markdown(f"""
    # Relatório de Análise de Dados
    **Data:** {datetime.now().strftime("%d/%m/%Y %H:%M")}  
    **Dataset:** {df.shape[0]} linhas, {df.shape[1]} colunas  
    **Tipo de dados:** {analysis_results['data_info']['data_type']}  
    **Problema identificado:** {analysis_results['data_info']['problem_type']}  
    """)
    
    # Sumário executivo
    st.markdown("## 📌 Sumário Executivo")
    
    if 'interpretation' in analysis_results['data_info']:
        st.write(analysis_results['data_info']['interpretation'])
    
    # Análise descritiva
    st.markdown("## 📊 Análise Descritiva")
    
    if 'descriptive' in analysis_results:
        desc = analysis_results['descriptive']
        st.write(f"- **Total de registros:** {desc['shape'][0]}")
        st.write(f"- **Variáveis numéricas:** {desc['numeric_columns']}")
        st.write(f"- **Variáveis categóricas:** {desc['categorical_columns']}")
        st.write(f"- **Valores ausentes:** {desc['missing_values']}")
        st.write(f"- **Duplicatas:** {desc['duplicates']}")
    
    # Análise preditiva
    if 'predictive' in analysis_results:
        st.markdown("## 🤖 Análise Preditiva")
        
        pred = analysis_results['predictive']
        st.write(f"- **Tipo de modelo:** {pred['model_type']}")
        
        if pred['model_type'] == "Classificação":
            st.write(f"- **Acurácia:** {pred['metrics']['accuracy']:.3f}")
            st.write(f"- **Precisão:** {pred['metrics']['precision']:.3f}")
            st.write(f"- **Recall:** {pred['metrics']['recall']:.3f}")
            st.write(f"- **F1-Score:** {pred['metrics']['f1']:.3f}")
        else:
            st.write(f"- **R² Score:** {pred['metrics']['r2']:.3f}")
            st.write(f"- **RMSE:** {pred['metrics']['rmse']:.3f}")
            st.write(f"- **MAE:** {pred['metrics']['mae']:.3f}")
        
        st.write("\n**Variáveis mais importantes:**")
        for i, (feature, imp) in enumerate(pred['feature_importance']['feature_importance'].items()):
            if i >= 5: break
            st.write(f"- {feature}: {imp:.3f}")
    
    # Análise de sobrevivência
    if 'survival' in analysis_results:
        st.markdown("## ⏳ Análise de Sobrevivência")
        
        surv = analysis_results['survival']
        st.write(f"- **Tempo mediano de sobrevivência:** {surv['median_survival']:.1f} dias")
        st.write("- **Probabilidades de sobrevivência:**")
        for time, prob in surv['survival_probabilities'].items():
            st.write(f"  - {time} dias: {prob:.2%}")
        st.write(f"- **Eventos observados:** {surv['num_events']}")
        st.write(f"- **Dados censurados:** {surv['num_censored']}")
    
    # Conclusões e recomendações
    st.markdown("## 🎯 Conclusões e Recomendações")
    
    if 'interpretation' in analysis_results:
        st.write(analysis_results['interpretation'])
    else:
        st.write("""
        - Realizar análises complementares para confirmar os achados
        - Considerar a coleta de dados adicionais para melhorar a qualidade da análise
        - Validar os modelos preditivos com novos conjuntos de dados
        """)
    
    # Rodapé
    st.markdown("""
    ---
    *Relatório gerado automaticamente pelo SISADE - Sistema de Inteligência Estatística para Análise de Dados Epidemiológicos*
    """)
    
    # Opção para baixar o relatório
    report_text = str(analysis_results)
    b64 = base64.b64encode(report_text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="relatorio_sisade_{datetime.now().strftime("%Y%m%d")}.txt">⬇️ Baixar Relatório (TXT)</a>'
    st.markdown(href, unsafe_allow_html=True)
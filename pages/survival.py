import streamlit as st
from analysis.survival import perform_survival_analysis
from core.analyzer import SISADEAnalyzer
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt 
from config import COLOR_SECONDARY
from components.metrics import analysis_card

def perform_survival_analysis(df, time_col, event_col):
    """Realiza análise de sobrevivência com formatação melhorada"""
    results = {}
    df_surv = df[[time_col, event_col]].dropna()
    kmf = KaplanMeierFitter()
    kmf.fit(df_surv[time_col], df_surv[event_col])
    
    
    # Plota a curva de sobrevivência
    kmf.plot_survival_function()
    plt.title("Curva de Sobrevivência (Kaplan-Meier)")
    plt.xlabel("Tempo")
    plt.ylabel("Probabilidade de Sobrevivência")
    plt.show()  # Se estiver usando Streamlit, talvez precise ajustar
    
    #return kmf
    
    median_survival = kmf.median_survival_time_
    survival_values = kmf.survival_function_at_times([30, 90, 180, 365]).values.flatten()
    
    col1, col2 = st.columns(2)
    
    with col1:
        stats_content = f"""
        <div style="line-height: 1.6;">
            <p><strong style="color: {COLOR_SECONDARY};">Tempo mediano de sobrevivência:</strong> 
               <span style="font-weight: bold;">{median_survival:.1f} dias</span></p>
            
            <p style="margin-top: 15px;"><strong style="color: {COLOR_SECONDARY};">Probabilidade de sobrevivência:</strong></p>
            <ul style="margin-top: 5px; padding-left: 20px;">
                <li style="margin-bottom: 5px;">30 dias: <strong>{survival_values[0]:.2%}</strong></li>
                <li style="margin-bottom: 5px;">90 dias: <strong>{survival_values[1]:.2%}</strong></li>
                <li style="margin-bottom: 5px;">180 dias: <strong>{survival_values[2]:.2%}</strong></li>
                <li>365 dias: <strong>{survival_values[3]:.2%}</strong></li>
            </ul>
        </div>
        """
        analysis_card("📌 Estatísticas de Sobrevivência", stats_content)
    
    # ... (restante do código permanece igual)

def render_survival():
    """Renderiza a página de análise de sobrevivência"""
    # Verificar se há colunas para análise de sobrevivência
    time_cols = [col for col in st.session_state.df.columns if 'tempo' in col.lower() or 'time' in col.lower()]
    event_cols = [col for col in st.session_state.df.columns if 'evento' in col.lower() or 'status' in col.lower() or 'obito' in col.lower()]
    
    if len(time_cols) > 0 and len(event_cols) > 0:
        time_col = st.selectbox("Selecione a coluna de tempo:", time_cols)
        event_col = st.selectbox("Selecione a coluna de evento:", event_cols)
        
        if st.button("⏳ Executar Análise de Sobrevivência", key="run_survival"):
            surv_results = perform_survival_analysis(st.session_state.df, time_col, event_col)
            st.session_state.analysis_results['survival'] = surv_results
            
            # Interpretação dos resultados
            if st.session_state.api_key:
                analyzer = SISADEAnalyzer(st.session_state.api_key)
                with st.spinner("🤖 Interpretando resultados de sobrevivência..."):
                    interpretation = analyzer.interpret_results(surv_results, "Análise de Sobrevivência")
                    st.markdown("### 💡 Interpretação IA")
                    st.markdown(interpretation)
    else:
        st.warning("Não foram encontradas colunas adequadas para análise de sobrevivência (tempo + evento).")
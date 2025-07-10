import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from components.metrics import analysis_card

def perform_survival_analysis(df, time_col, event_col):
    """Realiza análise de sobrevivência"""
    results = {}
    
    # Filtrar dados válidos
    df_surv = df[[time_col, event_col]].dropna()
    
    # Kaplan-Meier
    kmf = KaplanMeierFitter()
    kmf.fit(df_surv[time_col], df_surv[event_col])
    
    # Plotar curva de sobrevivência
    plot_survival_curve(kmf)
    
    # Estatísticas resumidas
    median_survival = kmf.median_survival_time_
    survival_at_times = kmf.survival_function_at_times([30, 90, 180, 365])
    
    # Corrigir o acesso aos valores de sobrevivência
    survival_values = survival_at_times.values.flatten()  # Converte para array 1D
    
    col1, col2 = st.columns(2)
    
    with col1:
        stats_content = f"""
        - **Tempo mediano de sobrevivência:** {median_survival:.1f} dias
        - **Probabilidade de sobrevivência:**
          - 30 dias: {survival_values[0]:.2%}
          - 90 dias: {survival_values[1]:.2%}
          - 180 dias: {survival_values[2]:.2%}
          - 365 dias: {survival_values[3]:.2%}
        """
        analysis_card("📌 Estatísticas de Sobrevivência", stats_content)
    
    # ... (restante do código permanece igual)
    
    results.update({
        'median_survival': median_survival,
        'survival_probabilities': {
            '30_dias': survival_values[0],
            '90_dias': survival_values[1],
            '180_dias': survival_values[2],
            '365_dias': survival_values[3]
        },
        'num_events': df_surv[event_col].sum(),
        'num_censored': len(df_surv) - df_surv[event_col].sum()
    })
    
    return results

def plot_survival_curve(kmf):
    """Plota curva de sobrevivência"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=kmf.timeline,
        y=kmf.survival_function_['KM_estimate'],
        mode='lines',
        name='Estimativa KM'
    ))
    
    fig.add_trace(go.Scatter(
        x=kmf.timeline,
        y=kmf.confidence_interval_['KM_estimate_lower_0.95'],
        fill=None,
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=kmf.timeline,
        y=kmf.confidence_interval_['KM_estimate_upper_0.95'],
        fill='tonexty',
        mode='lines',
        line=dict(width=0),
        name='IC 95%'
    ))
    
    fig.update_layout(
        title='Curva de Sobrevivência (Kaplan-Meier)',
        xaxis_title='Tempo',
        yaxis_title='Probabilidade de Sobrevivência',
        hovermode='x'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def compare_survival_groups(df, time_col, event_col, group_col):
    """Compara sobrevivência entre grupos"""
    groups = df[group_col].dropna().unique()
    
    if len(groups) > 1:
        kmf = KaplanMeierFitter()
        fig = go.Figure()
        
        for group in groups:
            mask = (df[group_col] == group) & (~df[time_col].isna()) & (~df[event_col].isna())
            kmf.fit(df.loc[mask, time_col], df.loc[mask, event_col], label=str(group))
            fig.add_trace(go.Scatter(
                x=kmf.timeline,
                y=kmf.survival_function_['KM_estimate'],
                mode='lines',
                name=f'Grupo {group}'
            ))
        
        fig.update_layout(
            title=f'Curvas de Sobrevivência por {group_col}',
            xaxis_title='Tempo',
            yaxis_title='Probabilidade de Sobrevivência',
            hovermode='x'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Teste de log-rank para 2 grupos
        if len(groups) == 2:
            perform_logrank_test(df, time_col, event_col, group_col, groups)

def perform_logrank_test(df, time_col, event_col, group_col, groups):
    """Executa teste de log-rank entre dois grupos"""
    group1, group2 = groups
    mask1 = (df[group_col] == group1) & (~df[time_col].isna()) & (~df[event_col].isna())
    mask2 = (df[group_col] == group2) & (~df[time_col].isna()) & (~df[event_col].isna())
    
    results = logrank_test(
        df.loc[mask1, time_col],
        df.loc[mask2, time_col],
        event_observed_A=df.loc[mask1, event_col],
        event_observed_B=df.loc[mask2, event_col]
    )
    
    test_content = f"""
    **Teste de Log-Rank entre {group1} e {group2}:**
    - Estatística do teste: {results.test_statistic:.2f}
    - Valor p: {results.p_value:.4f}
    - Diferença {'significativa' if results.p_value < 0.05 else 'não significativa'} (α=0.05)
    """
    analysis_card("📊 Comparação de Grupos", test_content)
import streamlit as st

from config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_BACKGROUND

def metric_card(title, value, help_text=None):
    """Componente de card de métrica melhorado"""
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: {COLOR_PRIMARY}; margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 8px;">
            {title}
        </h3>
        <div style="font-size: 1.2rem; font-weight: bold; margin: 10px 0;">{value}</div>
        {f'<div style="font-size: 0.9rem; color: #666;">{help_text}</div>' if help_text else ''}
    </div>
    """, unsafe_allow_html=True)

def analysis_card(title, content):
    """Componente de card de análise melhorado"""
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: {COLOR_PRIMARY}; margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 8px;">
            {title}
        </h3>
        <div style="line-height: 1.6; margin-top: 10px;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)
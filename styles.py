import streamlit as st
from config import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_BACKGROUND

def load_css():
    st.markdown(f"""
    <style>
        .main-header {{
            background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_SECONDARY});
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .metric-card {{
            background: {COLOR_BACKGROUND};
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid {COLOR_PRIMARY};
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .metric-card h3 {{
            margin-top: 0;
            color: {COLOR_PRIMARY};
            font-size: 1.2rem;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }}
        
        .metric-card p, .metric-card ul, .metric-card li {{
            margin: 0.5rem 0;
            line-height: 1.6;
            font-size: 1rem;
        }}
        
        .metric-card ul {{
            padding-left: 1.5rem;
        }}
        
        .metric-card strong {{
            color: {COLOR_SECONDARY};
        }}
    </style>
    """, unsafe_allow_html=True)
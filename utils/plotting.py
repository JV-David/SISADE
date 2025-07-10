import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from sklearn.feature_selection import mutual_info_regression

def plot_correlation_matrix(data):
    """Plota matriz de correlação"""
    corr_matrix = data.corr()
    fig = px.imshow(corr_matrix,
                   text_auto=True,
                   color_continuous_scale='RdBu',
                   range_color=[-1, 1],
                   title='Matriz de Correlação')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig, use_container_width=True)

def plot_distribution(df, column):
    """Plota distribuição de uma variável"""
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(df, x=column, 
                          title=f'Histograma de {column}',
                          nbins=30)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(df, y=column, 
                    title=f'Boxplot de {column}')
        st.plotly_chart(fig, use_container_width=True)

def plot_feature_importance(model, feature_names):
    """Plota importância das features"""
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    fig = px.bar(feature_importance.head(10), 
                x='importance', y='feature',
                title='Top 10 Variáveis Mais Importantes',
                orientation='h')
    st.plotly_chart(fig, use_container_width=True)

def plot_mutual_info(X, y, feature_names, model_type, random_state):
    """Plota informação mútua"""
    if model_type == "Regressão":
        mi = mutual_info_regression(X, y, random_state=random_state)
    else:
        mi = mutual_info_classif(X, y, random_state=random_state)
    
    mi_df = pd.DataFrame({
        'feature': feature_names,
        'mutual_info': mi
    }).sort_values('mutual_info', ascending=False)
    
    fig = px.bar(mi_df.head(10), 
                x='mutual_info', y='feature',
                title='Top 10 Variáveis por Informação Mútua',
                orientation='h')
    st.plotly_chart(fig, use_container_width=True)
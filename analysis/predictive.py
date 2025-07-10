import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, mean_squared_error, 
                            r2_score, accuracy_score, confusion_matrix)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.impute import SimpleImputer
from components.metrics import analysis_card
from utils.plotting import plot_feature_importance, plot_mutual_info

def perform_predictive_analysis(df, target_col):
    """Realiza análise preditiva"""
    results = {}
    
    # Configurações da análise
    test_size = st.slider("Tamanho do conjunto de teste:", 0.1, 0.5, 0.2, 0.05)
    random_state = st.number_input("Random state:", 0, 100, 42)
    n_estimators = st.slider("Número de árvores:", 10, 200, 100, 10)
    max_depth = st.selectbox("Profundidade máxima:", [None, 5, 10, 20, 30])
    
    # Preparação dos dados
    with st.spinner("Preparando dados..."):
        df_clean = df.dropna(subset=[target_col])
        X = df_clean.drop(columns=[target_col])
        y = df_clean[target_col]
        
        # Codificar variáveis categóricas
        X_encoded, le_dict = encode_categorical_features(X)
        
        # Imputar e normalizar dados
        X_processed = preprocess_features(X_encoded)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = split_data(X_processed, y, test_size, random_state)
    
    # Treinar modelo
    model, model_type = train_model(X_train, y_train, n_estimators, max_depth, random_state)
    y_pred = model.predict(X_test)
    
    # Resultados
    if model_type == "Regressão":
        metrics = evaluate_regression(y_test, y_pred)
        plot_regression_results(y_test, y_pred)
    else:
        metrics = evaluate_classification(y_test, y_pred)
        plot_classification_results(y_test, y_pred)
    
    # Feature importance
    plot_feature_importance(model, X.columns)
    plot_mutual_info(X_processed, y, X.columns, model_type, random_state)
    
    results.update({
        'model_type': model_type,
        'metrics': metrics,
        'feature_importance': pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False).to_dict(),
        'predictions_made': len(y_pred)
    })
    
    return results

def encode_categorical_features(X):
    """Codifica features categóricas"""
    le_dict = {}
    for col in X.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        le_dict[col] = le
    return X, le_dict

def preprocess_features(X):
    """Preprocessa features (imputação e normalização)"""
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        X_imputed[numeric_cols] = scaler.fit_transform(X_imputed[numeric_cols])
    
    return X_imputed

def split_data(X, y, test_size, random_state):
    """Divide dados em treino e teste"""
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

def train_model(X_train, y_train, n_estimators, max_depth, random_state):
    """Treina modelo RandomForest apropriado"""
    if pd.api.types.is_numeric_dtype(y_train):
        model = RandomForestRegressor(n_estimators=n_estimators, 
                                    max_depth=max_depth, 
                                    random_state=random_state)
        model_type = "Regressão"
    else:
        model = RandomForestClassifier(n_estimators=n_estimators, 
                                     max_depth=max_depth, 
                                     random_state=random_state)
        model_type = "Classificação"
    
    model.fit(X_train, y_train)
    return model, model_type

def evaluate_regression(y_test, y_pred):
    """Avalia modelo de regressão"""
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mae = np.mean(np.abs(y_test - y_pred))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("R² Score", f"{r2:.3f}")
    col2.metric("RMSE", f"{rmse:.3f}")
    col3.metric("MAE", f"{mae:.3f}")
    
    return {
        'r2': r2,
        'rmse': rmse,
        'mae': mae
    }

def evaluate_classification(y_test, y_pred):
    """Avalia modelo de classificação"""
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Acurácia", f"{accuracy:.3f}")
    col2.metric("Precisão", f"{report['weighted avg']['precision']:.3f}")
    col3.metric("Recall", f"{report['weighted avg']['recall']:.3f}")
    col4.metric("F1-Score", f"{report['weighted avg']['f1-score']:.3f}")
    
    return {
        'accuracy': accuracy,
        'precision': report['weighted avg']['precision'],
        'recall': report['weighted avg']['recall'],
        'f1': report['weighted avg']['f1-score']
    }

def plot_regression_results(y_test, y_pred):
    """Plota resultados de regressão"""
    fig = px.scatter(x=y_test, y=y_pred, 
                    labels={'x': 'Valor Real', 'y': 'Valor Predito'},
                    title='Valores Reais vs Preditos')
    fig.add_shape(type='line', x0=y_test.min(), y0=y_test.min(),
                 x1=y_test.max(), y1=y_test.max(),
                 line=dict(color='red', dash='dash'))
    st.plotly_chart(fig, use_container_width=True)

def plot_classification_results(y_test, y_pred):
    """Plota resultados de classificação"""
    cm = confusion_matrix(y_test, y_pred)
    fig = px.imshow(cm, text_auto=True,
                   labels=dict(x="Predito", y="Real", color="Contagem"),
                   title="Matriz de Confusão")
    st.plotly_chart(fig, use_container_width=True)
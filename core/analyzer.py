import json
import google.generativeai as genai
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (classification_report, mean_squared_error, 
                            r2_score, accuracy_score)
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from utils.api_handlers import configure_gemini_api
from utils.data_validation import validate_data_for_analysis

class SISADEAnalyzer:
    def __init__(self, api_key):
        """Inicializa o analisador com configurações da API"""
        self.api_key = api_key
        self.model = None
        self.available = False
        self._configure_ai_model()
    
    def _configure_ai_model(self):
        """Configura o modelo de IA"""
        if self.api_key:
            try:
                configure_gemini_api(self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.available = True
            except Exception as e:
                raise Exception(f"Erro ao configurar API: {str(e)}")
    
    def analyze_data_structure(self, df):
        """Analisa a estrutura dos dados usando IA"""
        validate_data_for_analysis(df)
        
        if not self.available:
            return self._fallback_analysis(df)
        
        try:
            info = self._prepare_data_info(df)
            prompt = self._create_analysis_prompt(info)
            response = self._get_ai_response(prompt)
            return self._process_ai_response(response)
            
        except Exception as e:
            raise Exception(f"Erro na análise IA: {str(e)}")
    
    def _prepare_data_info(self, df):
        """Prepara informações sobre o dataset para análise"""
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'missing_values': df.isnull().sum().to_dict(),
            'sample_data': {col: list(df[col].head(3).values) for col in df.columns}
        }
    
    def _create_analysis_prompt(self, data_info):
        """Cria prompt para análise de dados"""
        return f"""
        Analise este dataset e identifique:
        1. O tipo de dados (epidemiológico, clínico, financeiro, etc.)
        2. Variáveis-alvo potenciais
        3. Análises estatísticas recomendadas
        4. Tipo de problema (classificação, regressão, etc.)
        5. Possíveis problemas nos dados
        
        Dados: {json.dumps(data_info, default=str, ensure_ascii=False)}
        
        Responda em formato JSON com as chaves:
        - data_type, target_variables, recommended_analyses,
        - problem_type, data_issues, interpretation
        """
    
    def _get_ai_response(self, prompt):
        """Obtém resposta da API de IA"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def _process_ai_response(self, response_text):
        """Processa a resposta da IA para extrair o JSON"""
        if '```json' in response_text:
            json_part = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            json_part = response_text.split('```')[1]
        else:
            json_part = response_text
            
        json_part = json_part.strip().replace("'", '"')
        return json.loads(json_part)
    
    def _fallback_analysis(self, df):
        """Análise de fallback sem IA"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Verifica se há colunas típicas de análise de sobrevivência
        survival_cols = []
        cols_lower = [col.lower() for col in df.columns]
        
        has_time_col = any('tempo' in col or 'time' in col for col in cols_lower)
        has_event_col = any('evento' in col or 'status' in col or 'obito' in col for col in cols_lower)
        
        if has_time_col and has_event_col:
            time_col = next(col for col in df.columns if 'tempo' in col.lower() or 'time' in col.lower())
            event_col = next(col for col in df.columns if 'evento' in col.lower() or 'status' in col.lower() or 'obito' in col.lower())
            survival_cols = [time_col, event_col]
        
        return {
            'data_type': 'Dataset genérico',
            'target_variables': numeric_cols[:3] if numeric_cols else categorical_cols[:1],
            'recommended_analyses': ['Estatística Descritiva', 'Correlação', 'Análise Preditiva'] + 
                                (['Análise de Sobrevivência'] if survival_cols else []),
            'problem_type': 'Regressão' if numeric_cols else 'Classificação',
            'data_issues': {
                'missing_values': df.isnull().sum().sum(),
                'duplicates': df.duplicated().sum()
            },
            'interpretation': 'Dataset com variáveis numéricas e categóricas para análise exploratória.'
        }
    
    def interpret_results(self, results, analysis_type):
        """Interpreta resultados usando IA"""
        if not self.available:
            return "Análise concluída. Verifique os gráficos e métricas acima."
        
        prompt = f"""
        Interprete os seguintes resultados de análise estatística de forma clara e acessível:
        
        Tipo de análise: {analysis_type}
        Resultados: {json.dumps(results, default=str, ensure_ascii=False)}
        
        Forneça uma interpretação em português, destacando:
        1. Principais achados (em negrito)
        2. Significância estatística (se aplicável)
        3. Implicações práticas para profissionais de saúde
        4. Limitações da análise
        5. Recomendações para próximos passos
        
        Use linguagem acessível para profissionais não-estatísticos e formate com markdown.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"**Erro na interpretação:** {str(e)}"
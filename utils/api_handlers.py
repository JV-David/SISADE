import google.generativeai as genai

def configure_gemini_api(api_key):
    """Configura a API do Gemini"""
    genai.configure(api_key=api_key)
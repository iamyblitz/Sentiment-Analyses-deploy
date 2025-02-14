import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import os
from backend.utilities import data_preprocessing
from frontend.utilities import sentiment_analysis

st.set_page_config(
    page_title="Анализ Тональности Текста",
    page_icon=":last_quarter_moon:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px 24px !important;
            border-radius: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# URL бэкенда через ngrok (или локальный URL для тестов)
BACKEND_URL = os.environ.get("BACKEND_URL") # URL по умолчанию и из переменной окружения

st.title("Анализ Тональности Текста")
st.write(
    "Определите эмоциональную окраску текста с использованием современных алгоритмов обработки естественного языка.")

st.sidebar.header("Режим работы")
app_mode = st.sidebar.radio(
    "Выберите режим:",
    ["Анализ тональности текста", "Очистка CSV данных"]
)

if app_mode == "Очистка CSV данных":
    data_preprocessing.data_preprocessing_ui(BACKEND_URL) # Вызываем UI функцию для data preprocessing

elif app_mode == "Анализ тональности текста":
    sentiment_analysis.sentiment_analysis_ui(BACKEND_URL) # Вызываем UI функцию для sentiment analysis
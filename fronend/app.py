import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import os

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
BACKEND_URL = os.environ.get("BACKEND_URL", "https://a9cd-77-238-242-109.ngrok-free.app") # URL по умолчанию и из переменной окружения

st.title("Анализ Тональности Текста")
st.write(
    "Определите эмоциональную окраску текста с использованием современных алгоритмов обработки естественного языка.")


def analyze_text_from_backend(text):
    api_url = f"{BACKEND_URL}/analyze_sentiment/"
    try:
        response = requests.post(api_url, json={"text": text})
        response.raise_for_status()  # Проверка на HTTP ошибки
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при запросе к бэкенду: {e}")
        return None


st.sidebar.header("Настройки анализа")
input_text = st.sidebar.text_area(
    "Введите текст для анализа:",
    "Мне очень нравится тут!"
)

analyze_button = st.sidebar.button("Анализировать текст")

st.sidebar.markdown("---")
st.sidebar.header("Демо-анализ")
demo_button = st.sidebar.button("Анализировать демо-тексты")

if analyze_button:
    if not input_text.strip():
        st.error("Пожалуйста, введите текст для анализа.")
    else:
        with st.spinner("Анализируем текст..."):
            result = analyze_text_from_backend(input_text)
            if result: # Проверяем, что результат не None
                sentiment = result["label"]
                score = result["score"]

                st.markdown("### Результат анализа")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write("**Тональность:**", sentiment)
                    st.write("**Уверенность:**", f"{score * 100:.2f}%")
                with col2:
                    st.progress(int(score * 100))
                st.markdown("#### Исходный текст")
                st.info(input_text)

if demo_button:
    sample_texts = [
        "Грустно!",
        "Так весело что плакать хочется(",
        "Продукт оправдывает ожидания.",
        "Скучная книга.",
        "Эта новость вызывает негативные эмоции."
    ]

    demo_results = []
    with st.spinner("Обрабатываем демо-тексты..."):
        for text in sample_texts:
            result = analyze_text_from_backend(text)
            if result: # Проверяем, что результат не None
                demo_results.append({"text": text, **result})

        if demo_results: # Проверяем, что есть результаты
            df_demo = pd.DataFrame(demo_results)

            st.markdown("### Анализ демо-текстов")
            st.dataframe(df_demo)

            sentiment_counts = df_demo["label"].value_counts().reset_index()
            sentiment_counts.columns = ["label", "count"]

            fig = px.bar(
                sentiment_counts,
                x="label",
                y="count",
                color="label",
                title="Распределение тональностей",
                labels={"label": "Тональность", "count": "Количество"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Не удалось получить результаты демо-анализа от бэкенда.")
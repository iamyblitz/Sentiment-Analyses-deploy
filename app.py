import streamlit as st
from transformers import pipeline
import plotly.express as px
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import threading

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



# Настройка блокировки для потокобезопасности
model_lock = threading.Lock()

st.title("Анализ Тональности Текста")
st.write(
    "Определите эмоциональную окраску текста с использованием современных алгоритмов обработки естественного языка.")


@st.cache_resource
def load_sentiment_model():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )


@st.cache_resource
def get_executor():
    return ThreadPoolExecutor(max_workers=4)


model = load_sentiment_model()
executor = get_executor()


def analyze_text(text):
    with model_lock:  # Блокировка для потокобезопасности модели
        return model(text)[0]


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
        future = executor.submit(analyze_text, input_text)
        with st.spinner("Анализируем текст..."):
            result = future.result()
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

    futures = [executor.submit(analyze_text, text) for text in sample_texts]

    with st.spinner("Обрабатываем демо-тексты..."):
        demo_results = [f.result() for f in futures]
        df_demo = pd.DataFrame([{
            "text": text,
            "label": res["label"],
            "score": res["score"]
        } for text, res in zip(sample_texts, demo_results)])

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
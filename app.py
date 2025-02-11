import streamlit as st
from transformers import pipeline
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Анализ Тональности Текста",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        h1 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size:16px;
            padding:10px 24px;
        }
    </style>
    """, unsafe_allow_html=True)


st.title("Анализ Тональности Текста")
st.write(
    "Определите эмоциональную окраску текста (положительная, отрицательная или нейтральная) с использованием современных алгоритмов обработки естественного языка.")



@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")


model = load_sentiment_model()


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
    if input_text.strip() == "":
        st.error("Пожалуйста, введите текст для анализа.")
    else:
        result = model(input_text)[0]
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
    for text in sample_texts:
        res = model(text)[0]
        demo_results.append({
            "text": text,
            "label": res["label"],
            "score": res["score"]
        })

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

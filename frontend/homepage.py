import streamlit as st


def load_video(video_path):
    """
    Загружает видеофайл в бинарном режиме.
    При возникновении ошибки выводит сообщение и возвращает None.
    """
    try:
        with open(video_path, "rb") as file:
            return file.read()
    except Exception as e:
        st.error(f"Не удалось загрузить видео '{video_path}': {e}")
        return None


def load_image(image_path):
    """
    Загружает изображение в бинарном режиме.
    При возникновении ошибки выводит сообщение и возвращает None.
    """
    try:
        with open(image_path, "rb") as file:
            return file.read()
    except Exception as e:
        st.error(f"Не удалось загрузить изображение '{image_path}': {e}")
        return None


def show_homepage():
    st.markdown("""
    <h1 style='text-align: center; margin-bottom: 5px;'>
        🐼 SentimentPanda: Твой детектив эмоций в текстах
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h4 style='text-align: center;'>
        Универсальная платформа для обработки и анализа текстовых данных 
        </h4> 
    """, unsafe_allow_html=True)
    st.markdown('\n\n')

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <style>
            .stButton > button {
                background: linear-gradient(45deg, #4CAF50, #8BC34A);
                color: white;
                border: none;
                padding: 20px 45px;
                border-radius: 25px;
                font-size: 1.4rem;
                height: 70px;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(76,175,80,0.4);
            }
            .stButton > button:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(76,175,80,0.6);
            }
        </style>
        """, unsafe_allow_html=True)

        if st.button("🚀 Начать анализ прямо сейчас!", use_container_width=True):
            st.experimental_set_query_params(page="app")

    st.markdown("\n---")

    # Пример использования изображения в блоке "Кастомизация модели"
    with st.expander("🤖 Кастомизация модели", expanded=False):
        st.markdown("""
        **Шаги:**
        1. Загрузите CSV-файл
        2. Нажмите "Обучить модель"
        3. Ознакомьтесь с результатами
        """)
        # Загружаем изображение через функцию load_image
        img_bytes = load_image("static/Training05.png")
        if img_bytes:
            st.image(img_bytes, width=1000)

    # Пример использования видео в других блоках
    with st.expander("📊 Анализ текста", expanded=False):
        st.markdown("""
        **Шаги:**
        1. Введите текст в поле ввода
        2. Нажмите "Анализировать"
        3. Ознакомьтесь с результатами
        """)
        video_bytes = load_video("static/analisys_text.mp4")
        if video_bytes:
            st.video(video_bytes, format="video/mp4", muted=True)

    with st.expander("🧹 Подготовка данных", expanded=False):
        st.markdown("""
        **Шаги:**
        1. Загрузите CSV-файл
        2. Выберите столбец с текстовыми данными
        3. Нажмите "Очистить CSV"
        4. Ознакомьтесь с результатами и скачайте итоговый файл
        """)
        video_bytes = load_video("static/clean_csv.mp4")
        if video_bytes:
            st.video(video_bytes, format="video/mp4", muted=True)

    with st.expander("🔍 Анализ CSV данных", expanded=False):
        st.markdown("""
        **Шаги:**
        1. Загрузите CSV-файл
        2. Выберите столбец для классификации
        3. Нажмите "Анализировать данные"
        4. Ознакомьтесь с результатами и скачайте размеченный файл
        """)
        video_bytes = load_video("static/analisys_csv.mp4")
        if video_bytes:
            st.video(video_bytes, format="video/mp4", muted=True)

    with st.expander("💬 Анализ чатов", expanded=False):
        st.markdown("""
        **Шаги:**
        1. Экспортируйте нужный вам чат по инструкции ниже
        2. Загрузите HTML-файл чата
        3. Нажмите "Анализировать чат"
        4. Ознакомьтесь с результатами
        """)
        video_bytes = load_video("static/analisys_chat.mp4")
        if video_bytes:
            st.video(video_bytes, format="video/mp4", muted=True)
        st.markdown("Как скачать чат из Telegram в формате HTML для анализа активности?")
        video_bytes = load_video("static/tgHTML.mp4")
        if video_bytes:
            st.video(video_bytes, format="video/mp4", muted=True)


# Для локального тестирования:
if __name__ == "__main__":
    show_homepage()

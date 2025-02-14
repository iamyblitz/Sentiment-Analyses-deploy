import re
from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class DataPreprocessor:
    def __init__(self, text_column='text'):
        self.text_column = text_column
        self.morph = MorphAnalyzer(lang='ru')

    def clean_text(self, text):
        text = re.sub(r'<[^>]*>', ' ', text, flags=re.MULTILINE)
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        text = re.sub(r'[^а-яА-ЯёЁ\s-]', ' ', text, flags=re.IGNORECASE)
        text = re.sub(r'[\s-]+', ' ', text)
        return text.strip().lower()

    def remove_stopwords(self, text, language='russian'):
        base_stopwords = set(stopwords.words(language))
        keep_words = {
            'не', 'ни', 'нет', 'без', 'никак', 'вовсе', 'отнюдь',  # Отрицания
            'очень', 'совсем', 'абсолютно', 'совершенно', 'крайне',  # Интенсификаторы
            'ли', 'ведь', 'либо', 'даже',  # Модальные частицы
            'хорошо', 'плохо', 'ужасно', 'прекрасно'  # Оценочные прилагательные
        }
        final_stopwords = base_stopwords - keep_words
        words = word_tokenize(text, language='russian')
        return ' '.join([w for w in words if w.lower() not in final_stopwords])

    def lemmatize_text(self, text):
        words = word_tokenize(text, language='russian')
        lemmas = []
        for word in words:
            parsed = self.morph.parse(word)[0]
            lemmas.append(parsed.normal_form)
        return ' '.join(lemmas)

    def preprocess_dataset(self, df):
        df[self.text_column] = df[self.text_column].str.replace(r'\b\d+\b', '')
        df[self.text_column] = df[self.text_column].apply(self.clean_text)
        df[self.text_column] = df[self.text_column].apply(self.remove_stopwords)
        df[self.text_column] = df[self.text_column].apply(self.lemmatize_text)
        df = df.dropna(subset=[self.text_column])
        return df

    def preprocess_text(self, text):
        text = re.sub(r'\b\d+\b', '', text)
        text = self.clean_text(text)
        text = self.remove_stopwords(text)
        text = self.lemmatize_text(text)
        return text



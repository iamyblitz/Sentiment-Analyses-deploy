from fastapi import FastAPI, HTTPException, Request,  UploadFile, File
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from transformers import pipeline
import threading
import pandas as pd
import io

from utilities.data_preprocessing import DataPreprocessor

app = FastAPI()

# Блокировка для потокобезопасности модели
model_lock = threading.Lock()
sentiment_pipeline = None

def load_sentiment_model():
    global sentiment_pipeline  # Используем глобальную переменную
    if sentiment_pipeline is None:
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
    return sentiment_pipeline

load_sentiment_model()

class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    label: str
    score: float

@app.post("/analyze_sentiment/", response_model=SentimentResponse)
async def analyze_sentiment(request: Request, text_request: TextRequest):
    try:
        with model_lock:  # Блокировка для потокобезопасности модели
            model = load_sentiment_model() # Получаем загруженную модель
            result = model(text_request.text)[0]
            return {"label": result["label"], "score": result["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/preprocess_csv/")
async def preprocess_csv(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8'))) # Читаем CSV из UploadFile

        data_preprocessor = DataPreprocessor() # Создаем экземпляр DataPreprocessor
        cleaned_df = data_preprocessor.preprocess_dataset(df.copy()) # Используем preprocess_dataset для очистки

        # Конвертируем DataFrame обратно в CSV строку
        output_stream = io.StringIO()
        cleaned_df.to_csv(output_stream, index=False)
        cleaned_csv_string = output_stream.getvalue()

        # Возвращаем CSV файл как StreamingResponse
        return StreamingResponse(
            io.StringIO(cleaned_csv_string),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment;filename=cleaned_data.csv"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
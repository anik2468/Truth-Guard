from fastapi import FastAPI, File, UploadFile, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from transformers import pipeline

import numpy as np
from PIL import Image
import requests
import os

import models
from database import engine, SessionLocal


# ---------------------------
# DATABASE
# ---------------------------

models.Base.metadata.create_all(bind=engine)


# ---------------------------
# FASTAPI APP
# ---------------------------

app = FastAPI(title="TruthGuard v3 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# ML MODEL
# ---------------------------

fake_news_model = pipeline(
    "text-classification",
    model="hamzab/roberta-fake-news-classification"
)


# ---------------------------
# REQUEST MODEL
# ---------------------------

class NewsInput(BaseModel):
    text: str


# ---------------------------
# DATABASE SESSION
# ---------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# NEWS API KEY (environment variable)
# ---------------------------

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# ---------------------------
# GOOGLE NEWS VERIFICATION
# ---------------------------

def check_google_news(query):

    if not NEWS_API_KEY:
        return False

    try:

        url = "https://newsapi.org/v2/everything"

        params = {
            "q": query,
            "language": "en",
            "pageSize": 10,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params, timeout=5)

        data = response.json()

        if "totalResults" in data and data["totalResults"] > 3:
            return True

        return False

    except Exception as e:
        print("News API Error:", e)
        return False


# ---------------------------
# HOME
# ---------------------------

@app.get("/")
def home():
    return {"message": "TruthGuard v3 Backend Running"}


# ---------------------------
# TEXT NEWS DETECTOR
# ---------------------------

@app.post("/check-news")
def check_news(data: NewsInput, db: Session = Depends(get_db)):

    text = data.text.strip()

    prediction = fake_news_model(text)[0]

    label = prediction["label"]
    confidence = prediction["score"]

    news_verified = check_google_news(text)

    if news_verified:
        result = "✅ Verified by News Sources"
        score = 90

    elif label == "FAKE" and confidence > 0.85:
        result = "⚠ Likely Fake News"
        score = int(confidence * 100)

    else:
        result = "⚠ Unverified Claim"
        score = int(confidence * 60)


    news = models.NewsCheck(
        text=text,
        result=result,
        score=score
    )

    db.add(news)
    db.commit()


    return {
        "result": result,
        "credibility_score": score,
        "ml_confidence": round(confidence, 3)
    }


# ---------------------------
# IMAGE METADATA CHECK
# ---------------------------

def check_metadata(image):

    try:
        exif = image.getexif()

        if exif is None or len(exif) == 0:
            return False

        return True

    except:
        return False


# ---------------------------
# IMAGE DETECTOR
# ---------------------------

@app.post("/check-image")
async def check_image(file: UploadFile = File(...), db: Session = Depends(get_db)):

    image = Image.open(file.file).convert("RGB")

    img_array = np.array(image)

    noise_score = float(np.std(img_array))

    metadata = check_metadata(image)


    if noise_score < 25:
        result = "⚠ Possible AI Generated Image"
        score = 40

    elif noise_score < 45:
        result = "⚠ Suspicious Image"
        score = 60

    else:
        result = "✅ Likely Real Image"
        score = 85


    if not metadata:
        score -= 10


    img = models.ImageCheck(
        filename=file.filename,
        result=result,
        score=score
    )

    db.add(img)
    db.commit()


    return {
        "result": result,
        "credibility_score": score,
        "noise_score": round(noise_score, 2),
        "metadata_present": metadata
    }
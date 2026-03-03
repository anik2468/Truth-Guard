from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Allow CORS for frontend communication

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsInput(BaseModel):
    text: str

fake_keywords = [
    "breaking",
    "shocking",
    "secret cure",
    "forward this",
    "government hiding"
]

@app.get("/")
def home():
    return {"message": "TruthGuard backend running"}

@app.post("/check-news")
def check_news(data: NewsInput):

    text = data.text.lower()

    score = 100

    for word in fake_keywords:
        if word in text:
            score -= 20

    if score < 60:
        result = "⚠ Likely Fake News"
    else:
        result = "✅ Possibly Real"

    return {
        "result": result,
        "credibility_score": score
    }
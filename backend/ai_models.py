from transformers import pipeline
import torch
import open_clip
from PIL import Image
import numpy as np

# Fake News Model
fake_news_model = pipeline(
    "text-classification",
    model="hamzab/roberta-fake-news-classification"
)

# CLIP model for image detection
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='laion2b_s34b_b79k'
)

def detect_fake_news(text):

    prediction = fake_news_model(text)[0]

    return prediction["label"], prediction["score"]


def detect_ai_image(image):

    img = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        features = model.encode_image(img)

    score = torch.norm(features).item()

    if score < 20:
        return "⚠ AI Generated Image", 40

    return "✅ Likely Real Image", 85


def calculate_noise(image):

    img_array = np.array(image)

    return np.std(img_array)
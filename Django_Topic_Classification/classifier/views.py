from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
from pathlib import Path

# Định nghĩa biến đường dẫn
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = r"E:\VN_Topic_Classification\topic_classification"
STOPWORDS_PATH = BASE_DIR / "vietnamese-stopwords.txt"

# Load mô hình và tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Danh sách nhãn
LABELS = ["Chính trị", "Kinh tế", "Văn hóa", "Thể thao", "Công nghệ"]

# Hàm tiền xử lý văn bản
def preprocess_text(text):
    stopwords = set()
    with open(STOPWORDS_PATH, "r", encoding="utf-8") as f:
        stopwords.update(line.strip() for line in f)
    
    text = text.lower()
    text = re.sub(r'\d+[h:\-/]\d*|\d+', '', text)
    text = re.sub(r'ngày|tháng|năm', '', text)
    words = text.split()
    text = " ".join(word for word in words if word not in stopwords)
    return " ".join(text.split())

# Hàm dự đoán
def predict_text(text):
    text = preprocess_text(text)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()[0]
    prediction = torch.argmax(outputs.logits, dim=-1).item()

    # Tạo dictionary màu sắc và icon cho từng nhãn
    label_styles = {
        "Chính trị": {"color": "green", "icon": "icons/politics.png"},
        "Kinh tế": {"color": "blue", "icon": "icons/economy.png"},
        "Văn hóa": {"color": "purple", "icon": "icons/culture.png"},
        "Thể thao": {"color": "orange", "icon": "icons/sports.png"},
        "Công nghệ": {"color": "red", "icon": "icons/technology.png"}
    }
    result = {
        "label": LABELS[prediction],
        "icon": label_styles[LABELS[prediction]]["icon"],  # Đường dẫn icon cho nhãn được dự đoán
        "probabilities": [
            {"label": LABELS[i], "prob": round(probs[i] * 100, 2), "color": label_styles[LABELS[i]]["color"]}
            for i in range(len(LABELS))
        ]
    }
    return result

# View xử lý
def index(request):
    result = None
    if request.method == "POST":
        text = request.POST.get("text", "")
        if text:
            result = predict_text(text)
    return render(request, "classifier/index.html", {"result": result})
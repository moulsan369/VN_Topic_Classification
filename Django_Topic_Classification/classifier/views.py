from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re

f_stop = "/vietnamese-stopwords.txt"
# Load mô hình và tokenizer
MODEL_PATH = "E:\CDTN\topic_classification"  
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Danh sách nhãn
LABELS = ["Chính trị", "Kinh tế", "Văn hóa", "Thể thao", "Công nghệ"]

# Hàm tiền xử lý văn bản
def preprocess_text(text):
    stopwords = set()
    # Đọc danh sách từ dừng từ file
    for file in ["f_stop"]:
        with open(file, "r", encoding="utf-8") as f:
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
    result = {
        "label": LABELS[prediction],
        "probabilities": {LABELS[i]: round(probs[i] * 100, 2) for i in range(len(LABELS))}
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
import glob
import json
import pandas as pd

# Đường dẫn đến 5 file JSON (thay bằng đúng đường dẫn bạn lưu file)
json_files = glob.glob("../Collecting_Data/Raw_Data/*.json")

data = []

# Đọc và gộp dữ liệu từ 5 file JSON
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        items = json.load(f)
        for item in items:
            title = item.get("title", "").strip()
            content = item.get("content", "").strip()
            label = item.get("label", "").strip()

            # Gộp title và content nếu hợp lệ
            if title and content and label:
                text = title + " " + content
                data.append({"text": text, "label": label})

# Tạo DataFrame
df = pd.DataFrame(data)

# Loại bỏ các dòng bị trùng nội dung + nhãn
df.drop_duplicates(subset=["text", "label"], inplace=True)

# Ghi ra file CSV
output_file = "../Collecting_Data/Raw_Data/train.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Đã lưu dữ liệu sạch vào: {output_file}")
print(f"Tổng số dòng sau khi làm sạch: {len(df)}")

# Kiểm tra số lượng mỗi nhãn
label_counts = df["label"].value_counts()
print("\nSố lượng bài theo từng nhãn:")
print(label_counts)

# Kiểm tra tổng cộng có đủ 5000 dòng và mỗi nhãn 1000 hay không
if len(df) == 5000 and all(label_counts == 1000):
    print("\n✅ Dữ liệu đầy đủ: 5000 dòng, mỗi nhãn có đúng 1000 bài.")
else:
    print("\n⚠️ Dữ liệu chưa đủ hoặc chưa cân bằng.")

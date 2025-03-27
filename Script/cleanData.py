import json
import os
from collections import Counter

# Đường dẫn thư mục chứa các file JSON
data_dir = "../Data/"
files = [
    "ChinhTri.json",
    "KinhTe.json",
    "VanHoa.json",
    "TheThao.json",
    "CongNghe.json"
]

# Danh sách để chứa dữ liệu đã làm sạch
cleaned_data = []
seen_titles = set()  # Để kiểm tra trùng lặp
valid_labels = {"Chính trị", "Kinh tế", "Văn hóa", "Thể thao", "Công nghệ"}

# Đọc và làm sạch từng file
for file_name in files:
    file_path = os.path.join(data_dir, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            title = item.get("title", "").strip()
            label = item.get("label", "").strip()

            # Kiểm tra tiêu đề và nhãn
            if (title and len(title) > 5 and  # Tiêu đề không rỗng, dài hơn 5 ký tự
                "Attention Required" not in title and  # Không chứa lỗi Cloudflare
                title not in seen_titles and  # Không trùng lặp
                label in valid_labels):  # Nhãn hợp lệ
                cleaned_data.append({"title": title, "label": label})
                seen_titles.add(title)

        print(f"Processed {file_name}: {len(data)} raw -> {len(cleaned_data) - len(seen_titles)} cleaned so far")

    except Exception as e:
        print(f"Error loading {file_name}: {e}")

# Lưu file đã làm sạch
output_file = "../Data/cleaned_data.json"
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(cleaned_data)} cleaned items to {output_file}")
except Exception as e:
    print(f"Error saving file: {e}")

# Thống kê nhãn
label_counts = Counter(item["label"] for item in cleaned_data)
print("Label distribution:", label_counts)
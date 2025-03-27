import json
import os

# Đường dẫn thư mục chứa các file JSON
data_dir = "../Data/"
files = [
    "ChinhTri.json",
    "KinhTe.json",
    "VanHoa.json",
    "TheThao.json",
    "CongNghe.json"
]

# Danh sách để chứa tất cả dữ liệu
all_data = []

# Đọc từng file và gộp
for file_name in files:
    file_path = os.path.join(data_dir, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)
        print(f"Loaded {len(data)} items from {file_name}")
    except Exception as e:
        print(f"Error loading {file_name}: {e}")

# Lưu thành file mới
output_file = "../Data/data_sc.json"
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(all_data)} items to {output_file}")
except Exception as e:
    print(f"Error saving file: {e}")
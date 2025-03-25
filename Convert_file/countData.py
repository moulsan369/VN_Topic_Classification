import json

# Đường dẫn file JSON gốc và file đầu ra
input_json = "../Urls_scraper/TheThao_scraper/thethao_urls.json"  # Thay bằng đường dẫn thực tế
output_json = "TheThao_urls_1000.json"

# Đọc file JSON gốc
with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lấy 1000 URL đầu tiên
limited_data = data[:1000]

# Ghi ra file JSON mới
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(limited_data, f, ensure_ascii=False, indent=4)

print(f"Đã cắt file xuống còn {len(limited_data)} URL và lưu vào {output_json}")
import json

# Đường dẫn file JSON và file TXT đầu ra
json_file = "E:\CDTN\ChinhTri_scraper\politics_urls.json"
txt_file = "ChinhTri_urls.txt"

# Đọc file JSON
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ghi URL ra file TXT (mỗi URL một dòng)
with open(txt_file, 'w', encoding='utf-8') as f:
    for item in data:
        url = item.get('url')  # Lấy giá trị 'url' từ mỗi mục
        if url:
            f.write(url + '\n')

print(f"Đã chuyển {len(data)} URL từ {json_file} sang {txt_file}")
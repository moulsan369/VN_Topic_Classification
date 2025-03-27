import json

# Đường dẫn file JSON và file TXT đầu ra
json_file = "../VanHoa_scraper/culture_urls.json"  # Điều chỉnh đường dẫn nếu cần
txt_file = "VanHoa_urls.txt"

# Đọc file JSON
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Giới hạn 1000 URL
url_limit = 1000
count = 0

# Ghi URL ra file TXT (mỗi URL một dòng, dừng khi đủ 1000)
with open(txt_file, 'w', encoding='utf-8') as f:
    for item in data:
        if count >= url_limit:
            break
        url = item.get('url')
        if url:
            f.write(url + '\n')
            count += 1

print(f"Đã chuyển {count} URL từ {json_file} sang {txt_file}")
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random

# Tự động tải ChromeDriver phù hợp với Chrome hiện tại
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Đọc file JSON chứa URL
input_json = "./ChinhTri_urls_1000.json"
with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)
urls = [item['url'] for item in data if 'url' in item]

# Danh sách lưu kết quả
results = []
title_limit = 1000
title_count = 0

# Crawl tiêu đề
try:
    for url in urls:
        if title_count >= title_limit:
            break
        
        driver.get(url)
        time.sleep(random.uniform(2, 5))
        
        title = driver.title
        if "Attention Required" not in title:
            results.append({
                'title': title.strip(),
                'label': 'Chính trị'
            })
            title_count += 1
            print(f"Crawled {title_count}/{title_limit}: {title}")
        else:
            print(f"Skipped blocked page: {url}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    with open("../Data/ChinhTri.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(results)} titles")
    driver.quit()
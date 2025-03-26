from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
import json
import time
import random

def init_driver():
    """Khởi tạo ChromeDriver mới"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.set_page_load_timeout(120) 
    return driver

# Khởi tạo driver ban đầu
driver = init_driver()

# Đọc file JSON chứa URL
input_json = "./TheThao_urls_1000.json"  # Điều chỉnh đường dẫn
with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)
urls = [item['url'] for item in data if 'url' in item]

# Danh sách lưu kết quả
results = []
title_limit = 1000
title_count = 0

# Crawl tiêu đề
try:
    for i, url in enumerate(urls):
        if title_count >= title_limit:
            break
        
        try:
            print(f"Attempting URL {i+1}/{len(urls)}: {url}")
            driver.get(url)
            time.sleep(random.uniform(2, 5))  # Đợi ngẫu nhiên 2-5 giây
            
            # Xác định tiêu đề dựa trên domain
            if 'vov.vn' in url:
                title = driver.title  # Lấy từ thẻ <title>
            elif 'vietnamnet.vn' in url:
                title_element = driver.find_element("css selector", "h1.content-detail-title")
                title = title_element.text if title_element else ""
            else:
                title = ""

            # Bỏ qua nếu bị chặn hoặc không có tiêu đề
            if title and "Attention Required" not in title:
                results.append({
                    'title': title.strip(),
                    'label': 'Thể thao'
                })
                title_count += 1
                print(f"Crawled {title_count}/{title_limit}: {title}")
            else:
                print(f"Skipped blocked or invalid page: {url}")

        except (TimeoutException, WebDriverException) as e:
            print(f"Error with {url}: {e}")
            driver.quit()  # Đóng driver cũ
            driver = init_driver()  # Khởi tạo driver mới
            continue

except Exception as e:
    print(f"Unexpected error: {e}")

finally:
    # Lưu kết quả
    output_json = "../Data/TheThao.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(results)} titles to {output_json}")
    
    # Đóng trình duyệt
    driver.quit()
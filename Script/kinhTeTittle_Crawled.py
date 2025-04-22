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
    driver.set_page_load_timeout(60)  # Timeout 60 giây
    return driver

# Khởi tạo driver ban đầu
driver = init_driver()

# Đọc file JSON chứa URL
input_json = "./KinhTe_urls_1000.json"
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
            
            if 'vov.vn' in url:
                title = driver.title
            elif 'baovanhoa.vn' in url:
                title_element = driver.find_element("css selector", "h1.detail__title")
                title = title_element.text if title_element else ""
            else:
                title = ""

            if title and "Attention Required" not in title:
                results.append({
                    'title': title.strip(),
                    'label': 'Kinh tế'
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
    with open("../Data/KinhTe.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(results)} titles to ../Data/KinhTe.json")
    driver.quit()
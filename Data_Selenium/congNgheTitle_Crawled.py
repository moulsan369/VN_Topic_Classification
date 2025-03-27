from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
import json
import time
import random

def init_driver():
    """Khởi tạo ChromeDriver mới"""
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")  # Bỏ qua lỗi SSL
        options.add_argument("--ignore-ssl-errors")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(120)
        return driver
    except Exception as e:
        print(f"Failed to initialize driver: {e}")
        return None

# Khởi tạo driver ban đầu
driver = init_driver()
if not driver:
    print("Initial driver setup failed. Exiting.")
    exit()

# Đọc file JSON chứa URL
input_json = "./CongNghe_urls_1000.json"  # Điều chỉnh đường dẫn
try:
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    urls = [item['url'] for item in data if 'url' in item]
except Exception as e:
    print(f"Error reading JSON file: {e}")
    driver.quit()
    exit()

# Danh sách lưu kết quả
results = []
title_limit = 1000
title_count = 0

# Crawl tiêu đề
for i, url in enumerate(urls):
    if title_count >= title_limit:
        break
    
    try:
        print(f"Attempting URL {i+1}/{len(urls)}: {url}")
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Đợi ngẫu nhiên 2-5 giây
        
        # Xác định tiêu đề dựa trên domain
        if 'vov.vn' in url or 'thanhnien.vn' in url:
            title = driver.title  # Lấy từ thẻ <title>
        elif 'vietnamnet.vn' in url:
            title_element = driver.find_element("css selector", "h1.content-detail-title")
            title = title_element.text if title_element else ""
        elif 'vnexpress.net' in url:
            title_element = driver.find_element("css selector", "h1.title-detail")
            title = title_element.text if title_element else ""
        else:
            title = ""

        # Bỏ qua nếu bị chặn hoặc không có tiêu đề
        if title and "Attention Required" not in title:
            results.append({
                'title': title.strip(),
                'label': 'Công nghệ'
            })
            title_count += 1
            print(f"Crawled {title_count}/{title_limit}: {title}")
        else:
            print(f"Skipped blocked or invalid page: {url}")

    except Exception as e:  # Bắt mọi lỗi
        print(f"Error with {url}: {e}")
        driver.quit()
        driver = init_driver()
        if not driver:
            print("Driver restart failed. Exiting.")
            break
        continue

# Lưu kết quả và đóng driver
try:
    output_json = "../Data/CongNghe.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(results)} titles to {output_json}")
except Exception as e:
    print(f"Error saving file: {e}")
finally:
    driver.quit()
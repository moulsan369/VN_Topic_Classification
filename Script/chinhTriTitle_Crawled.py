from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time
import random

# Cấu hình Chrome Options
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("accept-language=vi-VN,vi;q=0.9,en;q=0.8")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

# Tự động tải ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

# Đọc file JSON chứa URL
input_json = "../Collecting_Data/Collect_Urls/ChinhTri_urls.json"
with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)
urls = [item['url'] for item in data if 'url' in item]

# Danh sách lưu kết quả
results = []
content_limit = 1000
content_count = 0

# Crawl nội dung bài báo
try:
    for url in urls:
        if content_count >= content_limit:
            break
        
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # Delay 5-10 giây
        
        # Cuộn trang để tăng tính thật
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 3))
        driver.execute_script("window.scrollTo(0, 0);")
        
        title = driver.title
        if "Attention Required" in title:
            print(f"Skipped blocked page: {url}")
            continue
        
        try:
            # Chờ phần tử tải
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.article-content")))
            
            # Lấy nội dung từ các thẻ: div.row.article-content p, h3.card-title, h5.media-title
            content_elements = driver.find_elements(By.CSS_SELECTOR, "div.row.article-content p, h3.card-title, h5.media-title")
            content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
            
            if content:
                results.append({
                    'title': title.strip(),  # Thêm tiêu đề vào kết quả
                    'content': content,
                    'label': 'Chính trị'
                })
                content_count += 1
                print(f"Crawled {content_count}/{content_limit}: {url}")
            else:
                print(f"No content found for: {url}")

        except Exception as e:
            print(f"Error extracting content from {url}: {e}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    with open("../Collecting_Data/Raw_Data/ChinhTri_content.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(results)} articles")
    driver.quit()
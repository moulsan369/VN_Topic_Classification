from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import random
import os

def init_driver():
    """Khởi tạo ChromeDriver ở chế độ headless với các tùy chọn khắc phục lỗi"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-unsafe-swiftshader")  # Khắc phục lỗi WebGL
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    chrome_options.add_argument("accept-language=vi-VN,vi;q=0.9,en;q=0.8")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(5)  # Giảm thời gian chờ ngầm
    return driver

def save_results(results, output_file):
    """Lưu kết quả vào file JSON"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def scrape_article(driver, url, retries=2):
    """Cào dữ liệu tiêu đề và nội dung từ URL với cơ chế thử lại"""
    for attempt in range(retries):
        try:
            print(f"Đang cào URL: {url} (Lần thử {attempt + 1}/{retries})")
            driver.get(url)
            WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(random.uniform(3, 6))  # Đợi nội dung động

            title = ""
            content = ""

            # Lấy tiêu đề
            if 'vov.vn' in url:
                title = driver.title
                if not title:
                    title_element = driver.find_elements(By.CSS_SELECTOR, "h1.title, h1.article-title, h1")
                    title = title_element[0].text if title_element else ""
            elif 'baovanhoa.vn' in url:
                title_element = driver.find_elements(By.CSS_SELECTOR, "h1.detail__title, h1.title, h1.post-title, h1")
                title = title_element[0].text if title_element else driver.title

            # Lấy nội dung từ thẻ <p> trong các container phổ biến
            content_elements = driver.find_elements(By.CSS_SELECTOR, "article p, .content p, .article-content p, .detail__content p, div[class*='content'] p")
            content = " ".join([elem.text for elem in content_elements if elem.text.strip()])
            print(f"Tìm thấy {len(content_elements)} thẻ <p> cho {url}")

            # Fallback: lấy tất cả thẻ <p> trên trang
            if not content:
                content_elements = driver.find_elements(By.CSS_SELECTOR, "p")
                content = " ".join([elem.text for elem in content_elements if elem.text.strip()])
                print(f"Fallback: Tìm thấy {len(content_elements)} thẻ <p> trên toàn trang cho {url}")

            return {
                "title": title,
                "content": content,
                "label": "Kinh tế"
            }

        except (TimeoutException, WebDriverException) as e:
            print(f"Lỗi khi cào {url}: {str(e)}")
            if attempt == retries - 1:
                return {
                    "title": "",
                    "content": "",
                    "label": "Kinh tế",
                    "error": str(e)
                }
            time.sleep(random.uniform(2, 5))

def main():
    driver = init_driver()
    output_file = "../Collecting_Data/Raw_Data/KinhTe.json"
    results = []  # Bắt đầu từ đầu, không tải dữ liệu cũ

    try:
        input_json = "../Collecting_Data/Collect_Urls/KinhTe_urls_1000.json"
        with open(input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        urls = [item['url'] for item in data if 'url' in item]

        content_limit = 1000
        content_count = 0

        for i, url in enumerate(urls):
            if content_count >= content_limit:
                break

            result = scrape_article(driver, url)
            if result["title"] and result["content"]:  # Chỉ đếm nếu có cả title và content
                content_count += 1
                results.append(result)
                save_results(results, output_file)  # Lưu sau mỗi URL
                print(f"Đã cào {content_count}/{content_limit}: {result['title']}")
            else:
                print(f"Không tìm thấy tiêu đề hoặc nội dung cho: {url}")

        print(f"Hoàn tất! Đã lưu {len(results)} bài viết vào {output_file}")

    except KeyboardInterrupt:
        print("\nPhát hiện Ctrl+C, đang lưu kết quả trước khi thoát...")
        save_results(results, output_file)
        print(f"Đã lưu {len(results)} bài viết vào {output_file}")
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
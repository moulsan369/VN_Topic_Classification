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
    service = Service(ChromeDriverManager().install())  # Tự động tải lại ChromeDriver nếu cần
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    return driver

def save_results(results, output_file):
    """Lưu kết quả vào file JSON"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def load_existing_results(output_file):
    """Tải dữ liệu hiện có từ file JSON nếu tồn tại"""
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Cảnh báo: {output_file} bị lỗi hoặc rỗng. Bắt đầu với danh sách rỗng.")
            return []
    return []

def scrape_article(driver, url, retries=2):
    """Cào dữ liệu tiêu đề và nội dung từ URL với cơ chế thử lại"""
    for attempt in range(retries):
        try:
            print(f"Đang cào URL: {url} (Lần thử {attempt + 1}/{retries})")
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(random.uniform(3, 6))  # Tăng thời gian đợi cho nội dung động

            title = ""
            content = ""

            # Lấy tiêu đề
            if 'vov.vn' in url:
                title = driver.title
                if not title:
                    title_element = driver.find_elements(By.CSS_SELECTOR, "h1.title, h1.article-title, h1")
                    title = title_element[0].text if title_element else ""
            elif 'baovanhoa.vn' in url:
                title_element = driver.find_elements(By.CSS_SELECTOR, "h1.title, h1.post-title, h1")
                title = title_element[0].text if title_element else ""  # Sửa lỗi: dùng title_element thay vì title_elements

            # Lấy nội dung từ tất cả thẻ <p> trong các container phổ biến
            content_elements = driver.find_elements(By.CSS_SELECTOR, "article p, .content p, .article-content p, .post-content p, div[class*='content'] p, div[class*='article'] p")
            content = " ".join([elem.text for elem in content_elements if elem.text.strip()])
            print(f"Tìm thấy {len(content_elements)} thẻ <p> cho {url}")

            # Fallback: nếu không tìm thấy nội dung, lấy tất cả thẻ <p> trên trang
            if not content:
                content_elements = driver.find_elements(By.CSS_SELECTOR, "p")
                content = " ".join([elem.text for elem in content_elements if elem.text.strip()])
                print(f"Fallback: Tìm thấy {len(content_elements)} thẻ <p> trên toàn trang cho {url}")

            return {
                "url": url,  # Lưu URL để theo dõi các URL đã cào
                "title": title,
                "content": content,
                "label": "văn hoá"
            }

        except (TimeoutException, WebDriverException) as e:
            print(f"Lỗi khi cào {url}: {str(e)}")
            if attempt == retries - 1:
                return {
                    "url": url,
                    "title": "",
                    "content": "",
                    "label": "văn hoá",
                    "error": str(e)
                }
            time.sleep(random.uniform(2, 5))  # Đợi trước khi thử lại

def main():
    driver = init_driver()
    output_file = "culture_articles.json"
    results = load_existing_results(output_file)  # Tải dữ liệu hiện có
    processed_urls = {result.get("url") for result in results if result.get("url")}  # Tập hợp các URL đã cào

    try:
        input_json = "../Collecting_Data/Collect_Urls/VanHoa_urls_1000.json"
        with open(input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        urls = [item['url'] for item in data if 'url' in item]

        title_limit = 1000
        title_count = sum(1 for result in results if result.get("title"))  # Đếm số tiêu đề đã cào
        start_index = len(results)  # Bắt đầu từ vị trí cuối cùng trong kết quả

        print(f"Tiếp tục từ {start_index} URL đã xử lý. Đã thu thập {title_count}/{title_limit} tiêu đề.")

        for i, url in enumerate(urls[start_index:], start=start_index):
            if title_count >= title_limit:
                break

            if url in processed_urls:
                print(f"Bỏ qua URL đã xử lý: {url}")
                continue

            result = scrape_article(driver, url)
            if result["title"]:
                title_count += 1
            results.append(result)
            save_results(results, output_file)  # Lưu ngay sau mỗi URL
            print(f"Đã xử lý {i+1}/{len(urls)} URL")

        # Loại bỏ trường 'url' khỏi kết quả cuối cùng
        final_results = [{"title": r["title"], "content": r["content"], "label": r["label"]} 
                         for r in results if "title" in r]
        save_results(final_results, output_file)
        print(f"Kết quả cuối (không có URL) đã được lưu vào {output_file}")

    except KeyboardInterrupt:
        print("\nPhát hiện Ctrl+C, đang lưu kết quả trước khi thoát...")
        final_results = [{"title": r["title"], "content": r["content"], "label": r["label"]} 
                         for r in results if "title" in r]
        save_results(final_results, output_file)
        print(f"Kết quả đã được lưu vào {output_file}")
        raise  # Thoát chương trình

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
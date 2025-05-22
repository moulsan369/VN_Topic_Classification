from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import random

def init_driver(headless=False):
    """Khởi tạo ChromeDriver mới"""
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("accept-language=vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--headless")  # Chế độ headless (không hiển thị giao diện)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(120)
    driver.implicitly_wait(10)
    return driver

# Khởi tạo driver ban đầu
driver = init_driver(headless=False)  # Đặt thành False để xem quá trình crawl

# Đọc file JSON chứa URL
input_json = "../Collecting_Data/Collect_Urls/TheThao_urls_1000.json"  # Điều chỉnh đường dẫn
try:
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    urls = [item['url'] for item in data if 'url' in item]
except FileNotFoundError:
    print(f"Không tìm thấy file {input_json}")
    driver.quit()
    exit()

# Danh sách lưu kết quả
results = []
content_limit = 1000
content_count = 0

# Crawl tiêu đề và nội dung
try:
    for i, url in enumerate(urls):
        if content_count >= content_limit:
            break
        
        try:
            print(f"Đang xử lý URL {i+1}/{len(urls)}: {url}")
            driver.get(url)
            time.sleep(random.uniform(2, 4))  # Đợi ngẫu nhiên 2-4 giây
            
            # Cuộn trang để tải nội dung động
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*2/3);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            title = ""
            content = ""
            
            # VOV.vn - Dựa trên phân tích mã nguồn
            if 'vov.vn' in url:
                try:
                    # Thử lấy tiêu đề theo nhiều cách
                    try:
                        title_element = driver.find_element(By.CSS_SELECTOR, "h1.title, .vovvn-title")
                        title = title_element.text.strip()
                    except NoSuchElementException:
                        title = driver.title
                    
                    # Lấy nội dung - VOV.vn thường sử dụng class article-content cho phần nội dung
                    try:
                        # Đợi cho đến khi nội dung được tải
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".article-content"))
                        )
                        # Loại bỏ các phần không cần thiết trước khi lấy nội dung chính
                        content_elements = driver.find_elements(By.CSS_SELECTOR, ".article-content p:not(.author)")
                        content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
                    except (TimeoutException, NoSuchElementException):
                        # Thử cách khác nếu không tìm thấy class article-content
                        content_elements = driver.find_elements(By.CSS_SELECTOR, ".row.detail-content p, .row.article-content p")
                        content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
                
                except Exception as e:
                    print(f"Lỗi khi xử lý VOV: {str(e)}")
            
            # VietnamNet - Dựa trên phân tích mã nguồn
            elif 'vietnamnet.vn' in url:
                try:
                    # Thử lấy tiêu đề
                    try:
                        title_element = driver.find_element(By.CSS_SELECTOR, "h1.content-detail-title, h1.title, .ArticleDetail h1")
                        title = title_element.text.strip()
                    except NoSuchElementException:
                        title = driver.title
                    
                    # Lấy nội dung
                    try:
                        # VietnamNet sử dụng nhiều định dạng khác nhau cho nội dung
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".ArticleContent, .maincontent"))
                        )
                        
                        # Thử từng bộ chọn CSS cho nội dung
                        content_selectors = [
                            ".ArticleContent p", 
                            ".maincontent p", 
                            "#article_body p",
                            ".content-detail__summary p, .content-detail__content p"
                        ]
                        
                        for selector in content_selectors:
                            content_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if content_elements:
                                content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
                                if content:  # Nếu tìm thấy nội dung, thoát vòng lặp
                                    break
                    
                    except (TimeoutException, NoSuchElementException) as e:
                        print(f"Lỗi khi lấy nội dung VietnamNet: {str(e)}")
                
                except Exception as e:
                    print(f"Lỗi khi xử lý VietnamNet: {str(e)}")
            
            # Xử lý các domain khác nếu có
            else:
                print(f"Không hỗ trợ domain: {url}")
                continue
            
            # Bỏ qua nếu bị chặn hoặc không có tiêu đề/nội dung
            if title and content and "Attention Required" not in title:
                results.append({
                    'title': title.strip(),
                    'content': content,
                    'label': 'Thể thao',
                    'url': url
                })
                content_count += 1
                print(f"Đã crawl {content_count}/{content_limit}: {title}")
                
                # In thông tin ngắn gọn về nội dung đã lấy được
                content_preview = content[:100] + "..." if len(content) > 100 else content
                print(f"Nội dung: {content_preview}")
            else:
                print(f"Bỏ qua trang không hợp lệ: {url}")
                print(f"Tiêu đề: {title}")
                print(f"Nội dung có dữ liệu: {'Có' if content else 'Không'}")

        except (TimeoutException, WebDriverException) as e:
            print(f"Lỗi với URL {url}: {e}")
            driver.quit()  # Đóng driver cũ
            driver = init_driver(headless=False)  # Khởi tạo driver mới
            continue

except Exception as e:
    print(f"Lỗi không mong muốn: {e}")

finally:
    # Lưu kết quả
    output_json = "../Collecting_Data/Raw_Data/TheThao_content.json"
    try:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu {len(results)} bài viết vào {output_json}")
    except Exception as e:
        print(f"Lỗi khi lưu file: {str(e)}")
    
    # Đóng trình duyệt
    driver.quit()
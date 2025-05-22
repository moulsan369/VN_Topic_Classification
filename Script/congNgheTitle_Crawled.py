from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import random

# Cấu hình Chrome Options
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("accept-language=vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Tự động tải ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

# Đọc file JSON chứa URL
input_json = "../Collecting_Data/Collect_Urls/CongNghe_urls_1000.json"
try:
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    urls = [item['url'] for item in data if 'url' in item]
except FileNotFoundError:
    print(f"File {input_json} not found")
    driver.quit()
    exit()

# Danh sách lưu kết quả
results = []
content_limit = 1000
content_count = 0

# Crawl tiêu đề và nội dung
try:
    for url in urls:
        if content_count >= content_limit:
            break

        print(f"Processing: {url}")
        try:
            driver.get(url)
            time.sleep(random.uniform(2, 4))  # Giảm độ trễ một chút

            # Cuộn trang để tải nội dung động
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")

            # Kiểm tra trang bị chặn
            title = driver.title
            if any(blocked in title for blocked in ["Attention Required", "Access Denied", "Cloudflare"]):
                print(f"Blocked page detected: {url}")
                continue

            # Phần trích xuất dữ liệu theo từng trang web cụ thể
            title = ""
            content = ""

            # VOV
            if 'vov.vn' in url:
                try:
                    # Thử nhiều bộ chọn CSS khác nhau cho tiêu đề
                    title_selectors = ["h1.title", "h1.cms-title", "h1.article-title"]
                    for selector in title_selectors:
                        try:
                            title_element = driver.find_element(By.CSS_SELECTOR, selector)
                            title = title_element.text.strip()
                            if title:
                                break
                        except NoSuchElementException:
                            continue
                    
                    if not title:
                        title = driver.title
                    
                    # Nội dung bài viết
                    content_selectors = [
                        "div.article-content p", 
                        "div.detail-content p", 
                        "div.text-long p"
                    ]
                    
                    for selector in content_selectors:
                        content_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if content_elements:
                            content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
                            break
                            
                except Exception as e:
                    print(f"Error extracting VOV content: {str(e)}")

            # Thanh Niên
            elif 'thanhnien.vn' in url:
                try:
                    # Thử nhiều bộ chọn CSS khác nhau cho tiêu đề
                    title_selectors = ["h1.detail-title", "h1.story__heading", "h1.title-page"]
                    for selector in title_selectors:
                        try:
                            title_element = driver.find_element(By.CSS_SELECTOR, selector)
                            title = title_element.text.strip()
                            if title:
                                break
                        except NoSuchElementException:
                            continue
                    
                    if not title:
                        title = driver.title
                    
                    # Nội dung bài viết
                    content_selectors = [
                        "div#abody p", 
                        "div.detail-content p", 
                        "div.content p"
                    ]
                    
                    for selector in content_selectors:
                        content_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if content_elements:
                            content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
                            break
                            
                except Exception as e:
                    print(f"Error extracting Thanh Niên content: {str(e)}")

            # VietnamNet
            elif 'vietnamnet.vn' in url:
                try:
                    # Thử nhiều bộ chọn CSS khác nhau cho tiêu đề
                    title_selectors = ["h1.content-detail-title", "h1.title", "h1.ArticleTitle"]
                    for selector in title_selectors:
                        try:
                            title_element = driver.find_element(By.CSS_SELECTOR, selector)
                            title = title_element.text.strip()
                            if title:
                                break
                        except NoSuchElementException:
                            continue
                    
                    if not title:
                        title = driver.title
                    
                    # Nội dung bài viết
                    content_selectors = [
                        "div.maincontent p", 
                        "div.main-content p", 
                        "div#article_body p", 
                        "div.ArticleContent p"
                    ]
                    
                    for selector in content_selectors:
                        content_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if content_elements:
                            content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
                            break
                            
                except Exception as e:
                    print(f"Error extracting VietnamNet content: {str(e)}")

            # VnExpress
            elif 'vnexpress.net' in url:
                try:
                    # Thử nhiều bộ chọn CSS khác nhau cho tiêu đề
                    title_selectors = ["h1.title-detail", "h1.title-news", "h1.title_news_detail"]
                    for selector in title_selectors:
                        try:
                            title_element = driver.find_element(By.CSS_SELECTOR, selector)
                            title = title_element.text.strip()
                            if title:
                                break
                        except NoSuchElementException:
                            continue
                    
                    if not title:
                        title = driver.title
                    
                    # Nội dung bài viết - VnExpress thường dùng fck_detail cho nội dung chính
                    content_selectors = [
                        "div.fck_detail p", 
                        "article.fck_detail p", 
                        "div.content_detail p"
                    ]
                    
                    for selector in content_selectors:
                        content_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if content_elements:
                            content = " ".join([element.text.strip() for element in content_elements if element.text.strip()])
                            break
                            
                except Exception as e:
                    print(f"Error extracting VnExpress content: {str(e)}")

            else:
                print(f"Unsupported domain: {url}")
                continue

            # Lọc bỏ những bài không lấy được đủ tiêu đề và nội dung
            if title and content:
                results.append({
                    'title': title.strip(),
                    'content': content,
                    'label': 'Công nghệ'
                })
                content_count += 1
                print(f"Crawled {content_count}/{content_limit}: {title}")
            else:
                print(f"No title or content found for: {url}")

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            continue

except Exception as e:
    print(f"Fatal error occurred: {str(e)}")

finally:
    # Lưu kết quả vào file
    output_file = "../Collecting_Data/Raw_Data/CongNghe_content.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(results)} articles to {output_file}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
    
    # Đóng trình duyệt
    driver.quit()
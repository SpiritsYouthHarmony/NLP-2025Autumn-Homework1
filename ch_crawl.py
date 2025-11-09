import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re
import os
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# 保存目录
OUTPUT_DIR = "xinhuawang" # 新华网中文版
# OUTPUT_DIR = "renminwang" # 人民网中文版
os.makedirs(OUTPUT_DIR, exist_ok=True)

visited = set()
corpus = []

def fetch_page_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AcademicCrawler/1.0)'
        }
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 提取标题
        title = soup.title.text.strip() if soup.title else ""
        
        # 提取正文
        content = ""
        for p in soup.find_all('p'):
            content += p.get_text().strip() + "\n"
            return title + "\n" + content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""
    
def extract_all_links(seed_url):
    try:
        r = requests.get(seed_url, headers={'User-Agent': 'AcademicCrawler'})
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            full_url = urljoin(seed_url, a['href'].strip())
            # 只保留同域链接（避免跳转到外部网站）
            if full_url.startswith(('http://www.news.cn', 'https://www.news.cn',
                                    'http://politics.people.com.cn/', 'http://ent.people.com.cn/',
                                    'https://cpc.people.com.cn/', 'https://world.people.com.cn/',
                                    'http://health.people.com.cn/', 'http://opinion.people.com.cn/',
                                    'http://tw.people.com.cn/')):
                links.add(full_url)
        return list(links)
    except Exception as e:
        print(f"Link extraction failed: {e}")
        return []

def crawl_from_seed(seed_url, max_pages=1, delay=1):
    queue = [seed_url]
    while queue and len(corpus) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        
        # 判断是否为新闻详情页（含日期和长字符串）
        if '/2025' in url and len(url) > 50:  
            text = fetch_page_text(url)
            if text.strip():
                text = re.sub(r'\s+', ' ', text)
                corpus.append(text)
                # 保存到文件（按序号命名）
                filename = os.path.join(OUTPUT_DIR, f"xinhuawang_{len(corpus)}.txt")
                # filename = os.path.join(OUTPUT_DIR, f"renminwang_{len(corpus)}.txt")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Saved {len(corpus)}: {url}")
        else:
            # 如果是目录页，继续提取链接
            new_links = extract_all_links(url)
            queue.extend(new_links)
        
        time.sleep(delay)  

seed_url = "https://www.news.cn/" # 新华网中文版
# seed_url = "http://people.com.cn/" # 人民网中文版

crawl_from_seed(seed_url=seed_url, max_pages=1000, delay=0.2)
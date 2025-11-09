import os
import re
from collections import Counter
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def extract_words_from_folder(folder_path):
    """从指定文件夹提取所有英文单词"""
    all_english_words = []
    
    # 遍历文件夹中所有的 .txt 文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # 提取英文单词（连续的英文字母）
                    english_words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", content.lower())
                    all_english_words.extend(english_words)
            except Exception as e:
                print(f"读取文件 {file_path} 时出错: {e}")
    
    return all_english_words

def plot_top_words(words, title, filename):
    """绘制前10个单词的直方图"""
    top_words = Counter(words).most_common(10)
    
    if top_words:
        words_list, counts = zip(*top_words)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(words_list)), counts, color='blue')
        plt.xlabel('单词')
        plt.ylabel('出现次数')
        plt.title(title)
        plt.xticks(range(len(words_list)), words_list, rotation=45, ha='right')
        
        # 在每个柱子上显示具体数值
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(filename)
        plt.show()
    else:
        print("未找到任何英文单词")

# 处理 en.people 文件夹
en_people_words = extract_words_from_folder("en.people")
print("en.people 文件夹中出现频率最高的10个英文单词:")
en_people_top10 = Counter(en_people_words).most_common(10)
for i, (word, count) in enumerate(en_people_top10, 1):
    print(f"{i:2d}. {word:<15} : {count:>6} 次")

plot_top_words(en_people_words, 'en.people文件夹中出现频率最高的10个英文单词', 'en_people_top10.png')

# 处理 english.news 文件夹
english_news_words = extract_words_from_folder("english.news")
print("\nenglish.news 文件夹中出现频率最高的10个英文单词:")
english_news_top10 = Counter(english_news_words).most_common(10)
for i, (word, count) in enumerate(english_news_top10, 1):
    print(f"{i:2d}. {word:<15} : {count:>6} 次")

plot_top_words(english_news_words, 'english.news文件夹中出现频率最高的10个英文单词', 'english_news_top10.png')

# 合并两个文件夹的内容
combined_words = en_people_words + english_news_words
print("\n合并后出现频率最高的10个英文单词:")
combined_top10 = Counter(combined_words).most_common(10)
for i, (word, count) in enumerate(combined_top10, 1):
    print(f"{i:2d}. {word:<15} : {count:>6} 次")

plot_top_words(combined_words, '合并后出现频率最高的10个英文单词', 'combined_top10.png')
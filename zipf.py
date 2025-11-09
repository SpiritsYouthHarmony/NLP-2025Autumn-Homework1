import os
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def extract_words_from_folder(folder_path):
    """从指定文件夹提取所有英文单词"""
    all_english_words = []
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    
    for filename in txt_files:
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                # 提取英文单词（连续的英文字母）
                english_words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", text.lower())
                all_english_words.extend(english_words)
        except Exception as e:
            print(f"⚠️ 读取文件 {filepath} 时出错：{e}")
    
    return all_english_words

def plot_zipf_law_log_scale(word_freq_pairs, title, filename):
    """绘制齐夫定律图：使用对数坐标轴"""
    # 提取排名和频率
    ranks = range(1, len(word_freq_pairs) + 1)
    frequencies = [freq for word, freq in word_freq_pairs]
    
    # 绘制图形
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, 'o', alpha=0.7, markersize=4, label='数据点')
    

    start_idx = 0  
    end_idx = len(ranks) 
    
    if end_idx > start_idx:
        sub_ranks = ranks[start_idx:end_idx]
        sub_frequencies = frequencies[start_idx:end_idx]
        
        # 计算对数空间中的线性回归
        log_ranks = np.log(sub_ranks)
        log_frequencies = np.log(sub_frequencies)
        
        coeffs = np.polyfit(log_ranks, log_frequencies, 1)
        poly1d_fn = np.poly1d(coeffs)
        
        # 在整个范围内绘制趋势线
        full_log_ranks = np.log(ranks)
        trend_line = np.exp(poly1d_fn(full_log_ranks))
        
        plt.loglog(ranks, trend_line, '--r', linewidth=2, 
                  label=f'趋势线')
                
    else:
        # 如果数据点太少，直接使用所有数据
        log_ranks = np.log(ranks)
        log_frequencies = np.log(frequencies)
        coeffs = np.polyfit(log_ranks, log_frequencies, 1)
        poly1d_fn = np.poly1d(coeffs)
        trend_line = np.exp(poly1d_fn(log_ranks))
        plt.loglog(ranks, trend_line, '--r', linewidth=2, 
                  label=f'趋势线')
    
    # 添加网格线
    plt.grid(True, which="both", ls="-", alpha=0.3)
    
    # 设置标签和标题
    plt.xlabel('排名')
    plt.ylabel('频率')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
    
    return coeffs[0]  # 返回斜率

# 处理 english.news 文件夹
print("正在处理 english.news 文件夹...")
english_news_words = extract_words_from_folder("english.news")
english_news_counter = Counter(english_news_words)
english_news_word_freq = english_news_counter.most_common(1000)  # 取前1000个词

if english_news_word_freq:
    slope1 = plot_zipf_law_log_scale(
        english_news_word_freq, 
        'english.news 齐夫定律验证 (对数坐标)', 
        'english_news_zipf_log.png'
    )
    print(f"english.news 斜率: {slope1:.2f}")

# 处理 en.people 文件夹
print("\n正在处理 en.people 文件夹...")
en_people_words = extract_words_from_folder("en.people")
en_people_counter = Counter(en_people_words)
en_people_word_freq = en_people_counter.most_common(1000)  # 取前1000个词

if en_people_word_freq:
    slope2 = plot_zipf_law_log_scale(
        en_people_word_freq, 
        'en.people 齐夫定律验证 (对数坐标)', 
        'en_people_zipf_log.png'
    )
    print(f"en.people 斜率: {slope2:.2f}")

# 合并两个文件夹的内容
print("\n正在处理合并后的数据...")
combined_words = english_news_words + en_people_words
combined_counter = Counter(combined_words)
combined_word_freq = combined_counter.most_common(1000)  # 取前1000个词

if combined_word_freq:
    slope3 = plot_zipf_law_log_scale(
        combined_word_freq, 
        '合并数据齐夫定律验证 (对数坐标)', 
        'combined_zipf_log.png'
    )
    print(f"合并数据斜率: {slope3:.2f}")
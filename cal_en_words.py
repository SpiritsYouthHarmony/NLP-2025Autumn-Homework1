import os
import re
import math
from collections import Counter
import matplotlib.pyplot as plt

def extract_english_words_from_folder(folder_path):
    """从指定文件夹中提取所有txt文件的英文单词"""
    all_english_words = []
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    
    for filename in txt_files:
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                # 使用更精确的正则表达式提取英文单词
                # 匹配由字母、数字、撇号和连字符组成的单词，但不以撇号或连字符开头或结尾
                english_words = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", text)
                all_english_words.extend(english_words)
        except Exception as e:
            print(f"⚠️ 读取文件 {filepath} 时出错：{e}")
    
    return all_english_words

def calculate_entropy_for_subset(words, subset_size):
    """计算指定大小子集的信息熵"""
    if len(words) < subset_size:
        subset = words
    else:
        subset = words[:subset_size]
    
    # 统计每个英文单词的频次
    word_counts = Counter(subset)
    total = sum(word_counts.values())
    
    # 计算信息熵
    entropy = 0.0
    for count in word_counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    
    return entropy

def plot_entropy_vs_scale(scales, entropies, title, filename):
    """绘制熵随样本规模变化的图表"""
    plt.figure(figsize=(10, 6))
    plt.plot(scales, entropies, marker='o')
    plt.xlabel('样本规模 (单词数)')
    plt.ylabel('信息熵 (比特/单词)')
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def process_single_folder(folder_path, scales, title_prefix):
    """处理单个文件夹并生成图表"""
    print(f"正在处理文件夹: {folder_path}")
    
    # 提取所有英文单词
    all_words = extract_english_words_from_folder(folder_path)
    print(f"总共提取到 {len(all_words)} 个英文单词")
    
    # 计算不同规模下的信息熵
    entropies = []
    valid_scales = []
    
    for scale in scales:
        if scale <= len(all_words):
            entropy = calculate_entropy_for_subset(all_words, scale)
            entropies.append(entropy)
            valid_scales.append(scale)
            print(f"规模 {scale}: 熵 = {entropy:.4f} 比特/单词")
        else:
            print(f"警告: 请求规模 {scale} 超过了实际单词总数 {len(all_words)}")
            break
    
    # 绘制图表
    if valid_scales:
        plot_entropy_vs_scale(
            valid_scales, 
            entropies, 
            f'{title_prefix}信息熵随样本规模变化', 
            f'{folder_path}_words_entropy.png'
        )
    
    return all_words

def main():
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 处理 english.news 文件夹 (5w, 10w, ..., 35w)
    english_news_scales = [i * 50000 for i in range(1, 8)]  # 5万, 10万, ..., 35万
    english_news_words = process_single_folder(
        "english.news", 
        english_news_scales, 
        "新华网英文版（单词）"
    )
    
    # 处理 en.people 文件夹 (5w, 10w, ..., 35w)
    en_people_scales = [i * 50000 for i in range(1, 8)]  # 5万, 10万, ..., 35万
    en_people_words = process_single_folder(
        "en.people", 
        en_people_scales, 
        "人民网英文版（单词）"
    )
    
    # 合并两个文件夹的内容并处理 (5w, 10w, 15w, ..., 75w)
    combined_words = english_news_words + en_people_words
    print(f"\n合并后总单词数: {len(combined_words)}")
    
    combined_scales = [i * 50000 for i in range(1, 16)]  # 5万, 10万, ..., 75万
    combined_entropies = []
    combined_valid_scales = []
    
    print("\n正在处理合并后的数据:")
    for scale in combined_scales:
        if scale <= len(combined_words):
            entropy = calculate_entropy_for_subset(combined_words, scale)
            combined_entropies.append(entropy)
            combined_valid_scales.append(scale)
            print(f"规模 {scale}: 熵 = {entropy:.4f} 比特/单词")
        else:
            print(f"警告: 请求规模 {scale} 超过了实际单词总数 {len(combined_words)}")
            break
    
    # 绘制合并数据的图表
    if combined_valid_scales:
        plot_entropy_vs_scale(
            combined_valid_scales,
            combined_entropies,
            '人民网+新华网英文版合并信息熵（单词）随样本规模变化',
            'combined_english_words_entropy.png'
        )

if __name__ == "__main__":
    main()
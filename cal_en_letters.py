import os
import re
import math
from collections import Counter
import matplotlib.pyplot as plt

def extract_english_letters_from_folder(folder_path):
    """从指定文件夹中提取所有txt文件的英文字母"""
    all_english_letters = []
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    
    for filename in txt_files:
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                # 只保留英文字母（a-z, A-Z）
                english_letters = re.findall(r'[a-zA-Z]', text)
                # 转换为小写统一处理
                english_letters = [letter.lower() for letter in english_letters]
                all_english_letters.extend(english_letters)
        except Exception as e:
            print(f"⚠️ 读取文件 {filepath} 时出错：{e}")
    
    return all_english_letters

def calculate_entropy_for_subset(letters, subset_size):
    """计算指定大小子集的信息熵"""
    if len(letters) < subset_size:
        subset = letters
    else:
        subset = letters[:subset_size]
    
    # 统计每个英文字母的频次
    letter_counts = Counter(subset)
    total = sum(letter_counts.values())
    
    # 计算信息熵
    entropy = 0.0
    for count in letter_counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    
    return entropy

def plot_entropy_vs_scale(scales, entropies, title, filename):
    """绘制熵随样本规模变化的图表"""
    plt.figure(figsize=(10, 6))
    plt.plot(scales, entropies, marker='o')
    plt.xlabel('样本规模 (字母数)')
    plt.ylabel('信息熵 (比特/字母)')
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def process_single_folder(folder_path, scales, title_prefix):
    """处理单个文件夹并生成图表"""
    print(f"正在处理文件夹: {folder_path}")
    
    # 提取所有英文字母
    all_letters = extract_english_letters_from_folder(folder_path)
    print(f"总共提取到 {len(all_letters)} 个英文字母")
    
    # 计算不同规模下的信息熵
    entropies = []
    valid_scales = []
    
    for scale in scales:
        if scale <= len(all_letters):
            entropy = calculate_entropy_for_subset(all_letters, scale)
            entropies.append(entropy)
            valid_scales.append(scale)
            print(f"规模 {scale}: 熵 = {entropy:.4f} 比特/字母")
        else:
            print(f"警告: 请求规模 {scale} 超过了实际字母总数 {len(all_letters)}")
            break
    
    # 绘制图表
    if valid_scales:
        plot_entropy_vs_scale(
            valid_scales, 
            entropies, 
            f'{title_prefix}信息熵随样本规模变化', 
            f'{folder_path}_entropy.png'
        )
    
    return all_letters

def main():
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 处理 english.news 文件夹 (30w, 60w, ..., 150w)
    english_news_scales = [i * 300000 for i in range(1, 6)]  # 30万, 60万, ..., 150万
    english_news_letters = process_single_folder(
        "english.news", 
        english_news_scales, 
        "新华网英文版"
    )
    
    # 处理 en.people 文件夹 (30w, 60w, ..., 150w)
    en_people_scales = [i * 300000 for i in range(1, 6)]  # 30万, 60万, ..., 150万
    en_people_letters = process_single_folder(
        "en.people", 
        en_people_scales, 
        "人民网英文版"
    )
    
    # 合并两个文件夹的内容并处理 (50w, 100w, 150w, ..., 400w)
    combined_letters = english_news_letters + en_people_letters
    print(f"\n合并后总字母数: {len(combined_letters)}")
    
    combined_scales = [i * 500000 for i in range(1, 9)]  # 50万, 100万, ..., 400万
    combined_entropies = []
    combined_valid_scales = []
    
    print("\n正在处理合并后的数据:")
    for scale in combined_scales:
        if scale <= len(combined_letters):
            entropy = calculate_entropy_for_subset(combined_letters, scale)
            combined_entropies.append(entropy)
            combined_valid_scales.append(scale)
            print(f"规模 {scale}: 熵 = {entropy:.4f} 比特/字母")
        else:
            print(f"警告: 请求规模 {scale} 超过了实际字母总数 {len(combined_letters)}")
            break
    
    # 绘制合并数据的图表
    if combined_valid_scales:
        plot_entropy_vs_scale(
            combined_valid_scales,
            combined_entropies,
            '人民网+新华网英文版合并信息熵随样本规模变化',
            'combined_english_entropy.png'
        )

if __name__ == "__main__":
    main()
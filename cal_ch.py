import os
import re
import math
from collections import Counter
import matplotlib.pyplot as plt

def extract_chinese_chars_from_folder(folder_path):
    """从指定文件夹中提取所有txt文件的中文字符"""
    all_chinese_chars = []
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    
    for filename in txt_files:
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                # 只保留中文汉字（\u4e00-\u9fa5）
                chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)
                all_chinese_chars.extend(chinese_chars)
        except Exception as e:
            print(f"⚠️ 读取文件 {filepath} 时出错：{e}")
    
    return all_chinese_chars

def calculate_entropy_for_subset(chars, subset_size):
    """计算指定大小子集的信息熵"""
    if len(chars) < subset_size:
        subset = chars
    else:
        subset = chars[:subset_size]
    
    # 统计每个汉字的频次
    char_counts = Counter(subset)
    total = sum(char_counts.values())
    
    # 计算信息熵
    entropy = 0.0
    for count in char_counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    
    return entropy

def plot_entropy_vs_scale(scales, entropies, title, filename):
    """绘制熵随样本规模变化的图表"""
    plt.figure(figsize=(10, 6))
    plt.plot(scales, entropies, marker='o')
    plt.xlabel('样本规模 (字符数)')
    plt.ylabel('信息熵 (比特/字)')
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def process_single_folder(folder_path, scales, title_prefix):
    """处理单个文件夹并生成图表"""
    print(f"正在处理文件夹: {folder_path}")
    
    # 提取所有中文字符
    all_chars = extract_chinese_chars_from_folder(folder_path)
    print(f"总共提取到 {len(all_chars)} 个中文字符")
    
    # 计算不同规模下的信息熵
    entropies = []
    valid_scales = []
    
    for scale in scales:
        if scale <= len(all_chars):
            entropy = calculate_entropy_for_subset(all_chars, scale)
            entropies.append(entropy)
            valid_scales.append(scale)
            print(f"规模 {scale}: 熵 = {entropy:.4f} 比特/字")
        else:
            print(f"警告: 请求规模 {scale} 超过了实际字符总数 {len(all_chars)}")
            break
    
    # 绘制图表
    if valid_scales:
        plot_entropy_vs_scale(
            valid_scales, 
            entropies, 
            f'{title_prefix}信息熵随样本规模变化', 
            f'{folder_path}_entropy.png'
        )
    
    return all_chars

def main():
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 处理 renminwang 文件夹 (10w, 20w, ..., 100w)
    renminwang_scales = [i * 100000 for i in range(1, 11)]  # 10万, 20万, ..., 100万
    renminwang_chars = process_single_folder(
        "renminwang", 
        renminwang_scales, 
        "人民网"
    )
    
    # 处理 xinhuawang 文件夹 (10w, 20w, ..., 100w)
    xinhuawang_scales = [i * 100000 for i in range(1, 11)]  # 10万, 20万, ..., 100万
    xinhuawang_chars = process_single_folder(
        "xinhuawang", 
        xinhuawang_scales, 
        "新华网"
    )
    
    # 合并两个文件夹的内容并处理 (20w, 40w, ..., 200w)
    combined_chars = renminwang_chars + xinhuawang_chars
    print(f"\n合并后总字符数: {len(combined_chars)}")
    
    combined_scales = [i * 200000 for i in range(1, 11)]  # 20万, 40万, ..., 200万
    combined_entropies = []
    combined_valid_scales = []
    
    print("\n正在处理合并后的数据:")
    for scale in combined_scales:
        if scale <= len(combined_chars):
            entropy = calculate_entropy_for_subset(combined_chars, scale)
            combined_entropies.append(entropy)
            combined_valid_scales.append(scale)
            print(f"规模 {scale}: 熵 = {entropy:.4f} 比特/字")
        else:
            print(f"警告: 请求规模 {scale} 超过了实际字符总数 {len(combined_chars)}")
            break
    
    # 绘制合并数据的图表
    if combined_valid_scales:
        plot_entropy_vs_scale(
            combined_valid_scales,
            combined_entropies,
            '人民网+新华网合并信息熵随样本规模变化',
            'combined_entropy.png'
        )

if __name__ == "__main__":
    main()
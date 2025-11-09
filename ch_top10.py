import os
import re
from collections import Counter
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def extract_chinese_chars_from_folder(folder_path):
    """从指定文件夹提取所有中文汉字"""
    all_chinese_chars = []
    
    # 遍历文件夹中所有的 .txt 文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # 提取中文汉字（Unicode范围：\u4e00-\u9fff）
                    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
                    all_chinese_chars.extend(chinese_chars)
            except Exception as e:
                print(f"读取文件 {file_path} 时出错: {e}")
    
    return all_chinese_chars

def plot_top_chars(chars, title, filename):
    """绘制前10个汉字的直方图"""
    top_chars = Counter(chars).most_common(10)
    
    if top_chars:
        chars_list, counts = zip(*top_chars)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(chars_list)), counts, color='skyblue')
        plt.xlabel('汉字')
        plt.ylabel('出现次数')
        plt.title(title)
        plt.xticks(range(len(chars_list)), chars_list)
        
        # 在每个柱子上显示具体数值
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(filename)
        plt.show()
    else:
        print("未找到任何中文汉字")

# 处理 renminwang 文件夹
renminwang_chars = extract_chinese_chars_from_folder("renminwang")
print("renminwang 文件夹中出现频率最高的10个中文汉字:")
renminwang_top10 = Counter(renminwang_chars).most_common(10)
for i, (char, count) in enumerate(renminwang_top10, 1):
    print(f"{i:2d}. {char:<15} : {count:>6} 次")

plot_top_chars(renminwang_chars, 'renminwang文件夹中出现频率最高的10个中文汉字', 'renminwang_top10.png')

# 处理 xinhuawang 文件夹
xinhuawang_chars = extract_chinese_chars_from_folder("xinhuawang")
print("\nxinhuawang 文件夹中出现频率最高的10个中文汉字:")
xinhuawang_top10 = Counter(xinhuawang_chars).most_common(10)
for i, (char, count) in enumerate(xinhuawang_top10, 1):
    print(f"{i:2d}. {char:<15} : {count:>6} 次")

plot_top_chars(xinhuawang_chars, 'xinhuawang文件夹中出现频率最高的10个中文汉字', 'xinhuawang_top10.png')

# 合并两个文件夹的内容
combined_chars = renminwang_chars + xinhuawang_chars
print("\n合并后出现频率最高的10个中文汉字:")
combined_top10 = Counter(combined_chars).most_common(10)
for i, (char, count) in enumerate(combined_top10, 1):
    print(f"{i:2d}. {char:<15} : {count:>6} 次")

plot_top_chars(combined_chars, '合并后出现频率最高的10个中文汉字', 'combined_top10.png')
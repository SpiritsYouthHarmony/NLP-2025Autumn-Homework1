import os
import re

def count_chinese_and_english_words(folder_path, english='words'):
    total_chinese_chars = 0
    total_english = 0
    
    # 遍历文件夹中所有的 .txt 文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # 统计汉字个数（中文字符范围：\u4e00-\u9fff）
                chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
                total_chinese_chars += len(chinese_chars)
                
                # 统计英文单词/字母个数
                if english == 'words':
                    english_matches = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", content)
                elif english == 'letters':
                    english_matches = re.findall(r"[a-zA-Z]", content)
                else:
                    english_matches = []
                
                total_english += len(english_matches)
    
    return total_chinese_chars, total_english



if __name__ == "__main__":
    # 定义要处理的文件夹路径（请根据实际路径修改）
    folders = [
        'en.people',
        'english.news',
        'renminwang',
        'xinhuawang'
    ]
    # 遍历每个文件夹并统计
    typename = 'words'  # 可选 'words' 或 'letters'
    for folder in folders:
        folder_path = os.path.join(folder)  
        if os.path.exists(folder_path):
            chinese_count, english_count = count_chinese_and_english_words(folder_path, english=typename)
            print(f"{folder}:")
            print(f"汉字个数: {chinese_count}")
            print("英文"+ typename + "个数" + f"{english_count}")
        else:
            print(f"文件夹 {folder} 不存在")
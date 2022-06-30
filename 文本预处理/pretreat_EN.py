import string
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import os

# 构建标点符号集
all_punc = string.punctuation

ifile_path = 'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\Org_EN\\'
ofile_path = 'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\New_EN\\'

files = os.listdir(ifile_path)
for file_name in files:
    txt = []
    with open(ifile_path + file_name, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            # sentence = ''
            for c in all_punc:
                line = line.replace(c, '')  # 删除所有标点符号

            line = line.lower()  # 转换成小写字母

            # 去除停用词
            word_list = [
                word for word in line.split() if word not in ENGLISH_STOP_WORDS
            ]

            porter_stemmer = PorterStemmer()
            singles = [porter_stemmer.stem(word) for word in word_list]
            sentence = ' '.join(singles)

            txt.append(sentence)
        f.close()

    ofile_name = ofile_path + 'New_' + file_name
    with open(ofile_name, "w") as file:  # 写入文件路径 + 章节名称 + 后缀
        for line in txt:
            file.write(line)

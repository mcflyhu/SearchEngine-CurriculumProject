import jieba
import string
import os

# 构建标点符号集
CN_punc = '，。、【】“”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=擅长于的&#@￥'
all_punc = string.punctuation + CN_punc

ifile_path = 'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\Org_CN\\'
ofile_path = 'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\New_CN\\'

files = os.listdir(ifile_path)
for file_name in files:
    txt = []
    with open(ifile_path + file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[1:]
        stopword = [
            line.strip() for line in
            open(ifile_path +
                 'CN_stopwords.txt', 'r', encoding='UTF-8').readlines()
        ]
        for line in lines:
            sentence = ''
            for c in all_punc:
                line = line.replace(c, '')  # 删除所有标点符号
            seg_list = jieba.cut_for_search(line)
            for word in seg_list:
                if word not in stopword:
                    sentence += word
            txt.append(sentence)
        f.close()

    ofile_name = ofile_path + 'New_' + file_name
    with open(ofile_name, "w", encoding='UTF-8') as file:  # 写入文件路径 + 章节名称 + 后缀
        for line in txt:
            file.write(line)

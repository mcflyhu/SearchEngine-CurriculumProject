import jieba
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


# 文本预处理，得到代表文章的字符串
def text_prtreat(file_path):
    # 构建标点符号集
    CN_punc = '，。、【】“”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=擅长于的&#@￥'
    all_punc = string.punctuation + CN_punc
    txt = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print('文档原文为：', lines)
        stopword = [
            line.strip() for line in open(
                'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\Org_CN\\CN_stopwords.txt',
                'r',
                encoding='UTF-8').readlines()
        ]
        for line in lines:
            sentence = ''
            for c in all_punc:
                line = line.replace(c, '')  # 删除所有标点符号
            seg_list = jieba.cut_for_search(line)  # 使用jieba分词
            for word in seg_list:
                if word not in stopword:  # 删除停用词
                    sentence += word + ' '  # 用空格隔开单词
            txt += sentence
        f.close()
    return txt


# 获取文档tf-idf矩阵
def getTfMatrix(document1, document2):
    corpus = []
    corpus.append(document1)
    corpus.append(document2)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)

    transformer = TfidfTransformer()
    tdidf = transformer.fit_transform(X)
    return tdidf.toarray()


def cosine(matrix):
    vector1 = matrix[0]
    vector2 = matrix[1]

    res = cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))
    return res[0, 0]


document1 = text_prtreat(
    'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\文本相似度\\doc1.txt')
document2 = text_prtreat(
    'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\文本相似度\\doc2.txt')

TfMatrix = getTfMatrix(document1, document2)
res = cosine(TfMatrix)
print('两文档之间的相似度为:', res)

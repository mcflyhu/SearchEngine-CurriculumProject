import string
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os


def text_preteat(file_path):
    txt = ''
    all_punc = string.punctuation
    with open(file_path, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
            for c in all_punc:
                line = line.replace(c, '')  # 删除所有标点符号

            line = line.lower()  # 转换成小写字母

            # 去除停用词
            word_list = [
                word for word in line.split() if word not in ENGLISH_STOP_WORDS
            ]

            txt += ' '.join(word_list)
        f.close()
    return txt


def getTfidfMatrix(corpus):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)

    transformer = TfidfTransformer()
    tdidf = transformer.fit_transform(X)
    return tdidf.toarray()


ifile_path = 'C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\Org_EN\\'

files = os.listdir(ifile_path)
corpus = []
cluster_result = pd.DataFrame(columns=['fileName'])
for file_name in files:
    document = text_preteat(ifile_path + file_name)
    corpus.append(document)
    cluster_result = cluster_result.append({'fileName': file_name},
                                           ignore_index=True)

X = getTfidfMatrix(corpus)
# print(X.shape)
# 进行KMeans聚类
clf_name = 'KMeans'
clf = KMeans(n_clusters=20)
X_train = clf.fit_transform(X)

# 统计聚类结果
print("聚类统计:")
cluster_result['label'] = clf.labels_
for name, group in cluster_result.groupby(['label']):
    print("第%d类簇中拥有%d个文档" % (name + 1, len(group)))

group = cluster_result.groupby('label')['fileName'].agg([('count', 'count')
                                                         ]).reset_index()
group = group.sort_values(by='count', ascending=False)

print("\r\n聚类形成的最大的3个类为：")
for index, row in group.iloc[:3].iterrows():
    print('第%d类拥有个%d文档' % (row['label'], row['count']))

distance = pd.DataFrame(X_train)
distance['label'] = clf.labels_
distance['fileName'] = cluster_result['fileName']

for name, group in distance.groupby('label'):
    group = group.sort_values(by=int(name), ascending=True)
    print("\r\n第%s类中最具代表性的五个文档为：" % (name))
    print(group.head(5)['fileName'])

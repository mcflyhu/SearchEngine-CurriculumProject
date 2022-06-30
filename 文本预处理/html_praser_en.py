import requests
from bs4 import BeautifulSoup
import re


def geturl():
    # 创建空的列表，存入每章节的url与章节名称
    words = []
    url_list = {
        "https://novel.tingroom.com/shuangyu/319/list.html",
        "https://novel.tingroom.com/jingdian/5018/list.html",
        "https://novel.tingroom.com/jingdian/5012/list.html",
        "https://novel.tingroom.com/jingdian/5004/list.html",
        'https://novel.tingroom.com/jingdian/4989/list.html',
        "https://novel.tingroom.com/jingdian/4983/list.html",
        'https://novel.tingroom.com/jingdian/4974/list.html',
        'https://novel.tingroom.com/jingdian/4967/list.html',
        'https://novel.tingroom.com/mingren/4761/list.html',
        'https://novel.tingroom.com/jingdian/4942/list.html',
        'https://novel.tingroom.com/jingdian/4940/list.html',
        'https://novel.tingroom.com/jingdian/4934/list.html',
        'https://novel.tingroom.com/jingdian/4933/list.html',
        'https://novel.tingroom.com/jingdian/4953/list.html',
        'https://novel.tingroom.com/jingdian/4946/list.html',
        'https://novel.tingroom.com/jingdian/4966/list.html',
        'https://novel.tingroom.com/jingdian/4921/list.html',
        'https://novel.tingroom.com/jingdian/4916/list.html',
        'https://novel.tingroom.com/jingdian/4907/list.html',
        'https://novel.tingroom.com/jingdian/4894/list.html',
        'https://novel.tingroom.com/jingdian/4892/list.html',
        'https://novel.tingroom.com/jingdian/4879/list.html',
        'https://novel.tingroom.com/jingdian/4852/list.html',
    }
    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }
    for url in url_list:
        req = requests.get(url=url, headers=header)
        req.encoding = req.apparent_encoding
        html = req.text
        bes = BeautifulSoup(html, "lxml")
        texts = bes.find("div", id="tt_text").find_all('li')

        # 对标签a内的内容进行提取
        for text in texts:
            url = url.replace('list.html', '')
            # print(url)
            url1 = url + text.find('a').get(
                "href")  # 获得每一章节小说的url，可从html代码中看到每一个"href"前边均缺少初始的url，因此需要加上
            word = [url1]  # 以列表格式存储
            words.append(word)  # 最终加入总的大列表中并返回
    # print(words)
    return words


if __name__ == '__main__':
    target = geturl()
    file_path = "C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\Org_EN\\"
    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }
    for i, tar in enumerate(target):
        req = requests.get(url=tar[0], headers=header, timeout=10)
        html = req.content.decode(req.apparent_encoding)
        print(tar[0])
        bes = BeautifulSoup(html, "lxml")
        texts = bes.find("div", id="tt_text")
        texts = texts.text
        texts = re.findall('[a-zA-z]+', texts)
        texts = ' '.join(texts)
        file_name = file_path + 'EN_' + '{0:03d}'.format(i) + '.txt'
        with open(file_name, "w",
                  encoding="UTF-8") as file:  # 写入文件路径 + 章节名称 + 后缀
            file.write(texts)

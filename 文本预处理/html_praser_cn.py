import requests
from bs4 import BeautifulSoup


def geturl():
    # 创建空的列表，存入每章节的url与章节名称
    words = []
    url_list = {
        "https://www.xqb5200.com/95_95204/",
        # "https://www.xqb5200.com/116_116844/",
        "https://www.xqb5200.com/116_116840/",
        # "https://www.xqb5200.com/109_109317/",
        # "https://www.xqb5200.com/111_111803/",
        #                                                                                                                                                                                                                                    "https://www.xqb5200.com/54_54197/",
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
        texts = bes.find("div", id="list")
        chapters = texts.find_all("a")  # 该函数可以返回list下的标签为a的所有信息

        # 对标签a内的内容进行提取
        for chapter in chapters:
            url1 = url + chapter.get(
                "href")  # 获得每一章节小说的url，可从html代码中看到每一个"href"前边均缺少初始的url，因此需要加上
            word = [url1]  # 以列表格式存储
            words.append(word)  # 最终加入总的大列表中并返回
        print(words)
    return words


if __name__ == '__main__':
    target = geturl()
    file_path = "C:\\Users\\McFly\\source\\VSCode\\搜索引擎\\Org_CN\\"
    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400"
    }
    for i, tar in enumerate(target):
        req = requests.get(url=tar[0], headers=header, timeout=5)
        req.encoding = 'gbk'
        html = req.text
        bes = BeautifulSoup(html, "lxml")
        texts = bes.find("div", id="content")
        texts_list = texts.text.split("\xa0" * 4)
        file_name = file_path + 'CN_' + '{0:03d}'.format(i) + ".txt"
        with open(file_name, "w",
                  encoding='utf-8') as file:  # 写入文件路径 + 章节名称 + 后缀
            for line in texts_list:
                file.write(line.replace('\xa0', '') + "\n")

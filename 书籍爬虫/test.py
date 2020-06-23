# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    target = 'https://www.biqukan.com/61_61498/476594994.html'
    req = requests.get(url=target)
    req.encoding = "gbk"
    html=req.content
    bf = BeautifulSoup(html)
    texts = bf.find_all('div', class_='showtxt')
    print("texts",texts)
    texts = texts[0].text.replace('\xa0' * 8, '\n\n')
    print(texts)
    # bf = BeautifulSoup(req.text)
    # texts = bf.find_all('div', class_='showtxt')
    # print(texts[0].text.replace('\xa0' * 8, '\n\n'))
    #print(texts)


    # path = './download'
    # fnamepath = path + '/一念永恒.txt'
    # fname = open(fnamepath, "w", encoding="utf-8")
    #
    # tempath = path + '/' + 1
    # x = open(tempath, "r", encoding="utf-8")  # 打开列表中的文件,读取文件内容
    # print(x)
    # fname.write(x.read())  # 写入新建的文件中
    # x.close()  # 关闭列表文件


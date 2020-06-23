# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests, sys, threading, os, shutil
import re  # 导入re模块
import xlwt
import chardet
from urllib import request
import random

"""
类说明:下载《笔趣看》网小说《一念永恒》
Parameters:
    无
Returns:
    无
Modify:
    2017-09-13
"""


class downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.target_child='https://www.biqukan.com/61_61498/476594994.html'
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数

    """
    函数说明:获取章节列表以及对应的下载链接列表
    Parameters:
        无
    Returns:
        无
    Modify:
        2017-09-13
    """


    def getHtml(url):  # 获取网页内容
        USER_AGENTS = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; \
            .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;\
                        .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko)\
                        Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) \
                       Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
                       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732;\
                        .NET4.0C; .NET4.0E; LBBROWSER)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; \
                       SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; \
                       Media Center PC 6.0; .NET4.0C; .NET4.0E)"]  # 浏览器(末尾附浏览器)
        proxies = []  # 代理IP（末尾附IP）
        req = request.Request(url)  # 设置url地址
        req.add_header('User-Agent', random.choice(USER_AGENTS))  # 随机选取浏览器
        # proxy_support = request.ProxyHandler({"http": random.choice(proxies)})  # 随机选取IP地址
        # opener = request.build_opener(proxy_support)  # 获取网站访问的对象
        # request.install_opener(opener)
        res = request.urlopen(req)  # 处理浏览器返回的对象
        html = res.read()
        return html

    def get_download_url(self):
        req = requests.get(url=self.target)
        req.encoding = "gbk"
        html = req.content
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])  # 剔除不必要的章节，并统计章节数
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    """
    函数说明:获取对应章节的内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2017-09-13
    """

    def get_contents(self,target):
        req = requests.get(url=target)
        req.encoding="gbk"
        html=req.content
        #print("html",html)
        #html = html.decode("gbk", 'replace').encode("utf-8")
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2017-09-13
    """

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, name, temdl, startNum, endNum):
        threading.Thread.__init__(self)
        self.runlist = list()
        self.name = name
        self.temdl = temdl
        self.startNum = startNum
        self.endNum = endNum

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        startDownloadTxt(self.temdl, self.startNum, self.endNum)
        print("Exiting " + self.name)


def mkdir(path):
    '''
    判断路径是否存在
    存在     True
    不存在   False
    '''
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def subFile(path):
    # 特定目录下的文件列表
    docList = os.listdir(path)
    # 显示当前文件夹下所有文件并进行排序
    '''
    key = lambda x:int(x[:-4])
    忽略文件名开始到倒数第四个字符为止
    docList.remove(i)
    删除数组中点开头的系统隐藏文件，因为会影响排序
    '''
    for i in docList:
        if (i[0] == '.'):
            docList.remove(i)
            break
    docList.sort(key=lambda x: int(x[:-4]))

    # 创建一个以书籍名字命名的文件
    fnamepath = path + '/一念永恒.txt'
    fname = open(fnamepath, "w","utf-8")
    # 打开你之前命名的下载文件
    for i in docList:
        tempath = path + '/' + i
        x = open(tempath, "r","utf-8")  # 打开列表中的文件,读取文件内容
        fname.write(x.read())  # 写入新建的文件中
        x.close()  # 关闭列表文件
    fname.close()

    # 移动最后的完成文件到桌面，在删除download文件夹(windows环境下根据情况自己修改路径)
    shutil.move(fnamepath, '/Users/chen/Desktop')
    shutil.rmtree(path)


'''
temdl:downloader类
startNum,endNum开始和结束的rang
'''


def startDownloadTxt(temdl, startNum, endNum):
    mkdir('download')
    for i in range(startNum, endNum):
        temPath = './download/' + str(i) + '.txt'
        temdl.writer(temdl.names[i], temPath, temdl.get_contents(temdl.urls[i]))
    print(temdl.names[i] + 'done')


if __name__ == "__main__":
    dl = downloader()
    # 获取章节列表以及对应的下载链接列表
    dl.get_download_url()
    #c= dl.get_contents()
    #print(c)
    print('《一年永恒》开始下载：')
    # 创建二十个线程(太多的话，会卡)
    threads = []
    threadNum = 20
    for p in range(threadNum):
        threadname = '"Thread' + str(p)
        stepNum = dl.nums // threadNum
        if (p == threadNum - 1):
            thread = myThread(threadname, dl, p * stepNum, dl.nums)
        else:
            thread = myThread(threadname, dl, p * stepNum, (p + 1) * stepNum)
        threads.append(thread)

    try:
        # 开启线程
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    except:
        print("Error: unable to start thread")

subFile('./download')
print('一念永恒下载完成')
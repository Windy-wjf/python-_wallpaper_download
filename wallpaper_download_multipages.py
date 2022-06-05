from fake_useragent import UserAgent
import requests
import random
import os
import sys
import re
import wget
import numpy as np
# re.findall匹配正则中所有符合的内容（输出元组）；
# re.finditer匹配正则中所有符合的内容（输出迭代器，效率高），for循环i.group()取出
# re.search全文匹配；i.group()取出
# re.match从头开始匹配，开头没有则停止，i.group()取出
max_pg_re = re.compile(r'<div class="pagination">.*?class="selected">1</span><a.*?>2</a>.*?>(?P<max_pg>.*?)</a><a',re.S)
message_list = ['aero','animals','architecture','girls','cute','nature','space','travel']
list = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0',\
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',\
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',\
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',\
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',\
        'Mozilla/5.0 (Windows NT 10.0; ............65.120 Safari/537.36 Core/1.77.66.400 QQBrowser/10.9.4603.400',\
        'Mozilla/5.0 (Linux; U; Android 10; zh-CN; SM-G9730 Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.2.0.1100 Mobile Safari/537.36',\
        'Mozilla/5.0 (Linux; U; Android 10; zh-CN; M2007J1SC Build/QKQ1.200419.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 UCBrowser/13.2.0.1100 Mobile Safari/537.36',\
        'Mozilla/5.0 (Linux; Android 10; V1829A Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/12.6 SP-engine/2.26.0 baiduboxapp/12.6.0.10 (Baidu; P1 10) NABar/1.0',\
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33']
headers = {'User-Agent':random.choice(list)}
#系统代理，可选
# os.environ["http_proxy"] = "http://127.0.0.1:1080"
# os.environ["https_proxy"] = "http://127.0.0.1:1080"
#根据要求下载壁纸
print("您可以选择以下这些分类来下载图片：aero,animals,architecture,girls,cute,nature,space,travel")
choice = str(input("请输入您选择的分类:"))
if choice in message_list:
    print("准备中，请稍候。")
else:
    print("输入出错，请按照要求输入！！！")
    sys.exit()
#获取每个分类的总页数，并输入自己要下载图片的页数
main_pg_url1='http://wallpaperswide.com/'+choice + '-desktop-wallpapers.html'#输入分类之后的页面网址，也是该分类下的第一页
main_pg = requests.get(url=main_pg_url1,headers=headers)
main_pg.encoding = 'utf-8'
main_pg_txt = main_pg.text
max_pg = max_pg_re.finditer(main_pg_txt)
for it in max_pg:
    max_page = int(it.group('max_pg'))
    print("该分类最多有%d页图片可供下载。"%max_page)
num_pg = int(input("请输入您要下载的图片页数(只能是整数)："))
#定义下载函数
def picdown_page(cat_page):#cat_page指的是每个分类下面的子页面的地址
    top = re.compile(r'<li class="wall" >.*?<a href="(?P<u1>.*?)" title="(?P<name>.*?)">', re.S)#定位每页每张图片的下载页面地址（ul）
    page = requests.get(url=cat_page, headers=headers)
    page.encoding = 'utf-8'
    page_txt = page.text
    res = top.finditer(page_txt)
    url = []#url里面存放着每页每张图片的下载页面地址（ul）的集合
    name = []
    for it in res:
        url.append("http://wallpaperswide.com"+it.group("u1"))

    # 根据头图(分类)地址获取每张图片的下载页面下HD最高清或者Standar最高清的下载地址并下载图片
    picdownhd = re.compile(r'<h3>HD.*?</h3>(?P<part>.*?)<br clear="all" />', re.S)#HD
    picdownst = re.compile(r'<h3>Standard 4:3</h3>(?P<part>.*?)<br clear="all" />', re.S)#standard 4：3
    picdownload = re.compile(r'<a target="_self" href="(?P<url>.*?)" title', re.S)
    parts = []
    u3 = []
    x = []
    n = 0
    for i in url:
        n += 1
        print("正在下载本页第%d张图片。"%n)
        # list列表中使用for循环时i指的是元素，而不是元素的下标
        pic = requests.get(url=i, headers=headers)
        pic.encoding = 'utf_8'
        pic_t = pic.text
        result = picdownhd.finditer(pic_t)
        parts = []
        for it in result:
            parts.append(it.group("part"))  # 注意迭代器必须用for循环取出
        if len(parts) != 0:
            u = picdownload.finditer(parts[0])#如果存在HD图片，则下载HD下最高清的图。否则下载standard下最高清的图片
        else:
            result = picdownst.finditer(pic_t)
            for it in result:
                parts.append(it.group("part"))
            u = picdownload.finditer(parts[0])
        u3 = []
        for j in u:
            u3.append("http://wallpaperswide.com"+j.group('url'))
        wget.download(u3[-1], "/home/wjf/图片/test/")#在此更改下载地址
        print("\n")
#开始根据输入的下载页数进行分类
if num_pg == 0:
    print("您选择了0页,啥也没下载，拜拜了您嘞！")
    sys.exit()
elif num_pg < 0:
    print("麻烦您别跟这搞笑，告辞！！！")
elif num_pg == 1:
    print("正在下载该分类下第1页的内容，请稍候。")
    picdown_page(main_pg_url1)
    print("共1页的内容下载完毕。")
else:
    print("正在下载该分类下共%d页的内容，请稍候。"%num_pg)
    x = np.arange(2,num_pg+1,1)
    print("正在下载该分类下第1页的内容...\n")
    picdown_page(main_pg_url1)
    for i in x:
        main_pg_urlx = 'http://wallpaperswide.com/'+choice + '-desktop-wallpapers/page/'+str(i)
        print("正在下载该分类下第%d页的内容..."%i)
        picdown_page(main_pg_urlx)
        print("第%d的内容下载完毕。"%i)
    print("共%d页的内容下载完毕。"%num_pg)

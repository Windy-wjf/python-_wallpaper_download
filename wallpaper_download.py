import requests
from bs4 import BeautifulSoup
import os
import sys
import re
import wget
# re.findall匹配正则中所有符合的内容（输出元组）；
# re.finditer匹配正则中所有符合的内容（输出迭代器，效率高），for循环i.group()取出
# re.search全文匹配；i.group()取出
# re.match从头开始匹配，开头没有则停止，i.group()取出
message_list = ['aero','animals','architecture','girls','cute','nature','spacce','travel']
# os.environ["http_proxy"] = "http://127.0.0.1:10081"
# os.environ["https_proxy"] = "http://127.0.0.1:10081"
#根据要求下载壁纸
print("可以选择以下这些选项：aero,animals,architecture,girls,cute,nature,space,travel")
choice = str(input("请输入您的下载选择:"))
if choice in message_list:
    print("下载准备中，请稍候！！！")
else:
    print("输入出错，请按照要求输入！！！")
    sys.exit()

page_url='http://wallpaperswide.com/'+choice + '-desktop-wallpapers.html'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
page = requests.get(url=page_url,headers=headers)
page.encoding = 'utf-8'
page_txt = page.text
# print(page_txt)
#定位头图地址
top = re.compile(r'<li class="wall" >.*?<a href="(?P<u1>.*?)" title="(?P<name>.*?)">',re.S)#惰性匹配：.*?  尽可能少地匹配
picdownload = re.compile(r'<h3>HD.*?</h3>.*?href="(?P<u2>)" title="',re.S)
res = top.finditer(page_txt)
url = []
name = []
for it in res:
    url.append("http://wallpaperswide.com"+it.group("u1"))
    name.append(it.group("name"))

# for i in url:
#     print(i)

#根据头图地址获取图片下载地址并下载图片
picdownhd = re.compile(r'<h3>HD.*?</h3>(?P<part>.*?)<br clear="all" />',re.S)
picdownst = re.compile(r'<h3>Standard 4:3</h3>(?P<part>.*?)<br clear="all" />',re.S)
picdownload = re.compile(r'<a target="_self" href="(?P<url>.*?)" title',re.S)
parts = []
u3 = []
x = []
for i in url:
    pic = requests.get(url=i,headers=headers)#list列表中使用for循环时i指的是元素，而不是元素的下标
    pic.encoding = 'utf_8'
    pic_t = pic.text
    result = picdownhd.finditer(pic_t)
    parts = []
    for it in result:
        parts.append(it.group("part"))#注意迭代器必须用for循环取出
    if len(parts)!=0:
        u = picdownload.finditer(parts[0])
    else:
        result = picdownst.finditer(pic_t)
        for it in result:
            parts.append(it.group("part"))
        u = picdownload.finditer(parts[0])
    u3 = []
    for j in u:
        u3.append("http://wallpaperswide.com"+j.group('url'))
    wget.download(u3[-1],"/home/wjf/图片/壁纸/")


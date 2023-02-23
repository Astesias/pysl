import re  # re模块主要包含了正则表达式
import urllib.request
from urllib import parse

from urllib import request  # urllib模块提供了读取Web页面数据的接口
import random

# 定义一个getHtml函数
def getHtml(url,headers):
    print('start-gethtml')
    # page = urllib.request.urlopen(url)  # urllib.request.urlopen()方法用于打开一个URL地址
    # html = page.read()  # read()方法用于读取URL上的数据
    page = urllib.request.Request(url, headers=headers)
    # page=requests.get(url, headers=headers)
    html=urllib.request.urlopen(page).read().decode("utf-8")
    if '网络不给力，请稍后重试' in html:
        print('failed')
        return html
    print('success')
    return html


# 图片下载
def getImg(html):
    reg = r'bpic="(.+?\.jpg)" class'  # 正则表达式，得到图片地址
    imgre = re.compile(reg)  # re.compile() 可以把正则表达式编译成一个正则表达式对象.
    # html = html  # python3
    imglist = re.findall(imgre, html)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
    print(imglist)

    # 把筛选的图片地址通过for循环遍历并保存到本地
    # 核心是urllib.request.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    x = 0
    for imgurl in imglist:
        urllib.request.urlretrieve(imgurl, r'D:\Desktop\.py\test\jpg\%s.jpg' % x)
        x += 1
    return x

if __name__ == '__main__':
    
    name='狗图'
    page=1
    
    user=['Mozilla/5.0 (compatible; MSIE 7.0; Windows CE; Trident/4.1)',
                'Mozilla/5.0 (Windows NT 4.0; ts-ZA; rv:1.9.0.20) Gecko/2012-10-04 01:55:52 Firefox/3.6.11',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.1)',
                'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/3.1)']
    headers = {'user-agent': random.choice(user),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    
    # h="https://tieba.baidu.com/f?ie=utf-8&kw=%E7%8C%AB%E5%9B%BE&fr=search"
    
    h="https://tieba.baidu.com/f?ie=utf-8&kw={}&fr=search".format(parse.quote(name))
    
    html = getHtml(h,headers)
    print('save {} jpgs'.format(getImg(html)))

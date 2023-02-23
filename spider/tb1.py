
# 导入需要的包
import time

# 模拟http请求 和 解析内容 的包
import requests
from urllib import parse
from bs4 import BeautifulSoup

# 数据展示 的包
import numpy as np
import pandas as pd
from pysl import getime
import urllib3  

# 设置点击量阈值
M = 300




# 从一页中提取 帖子
def extra_from_one_page(page_lst):
    '''从一页中提取 帖子'''
    # 临时列表保存字典数据，每一个帖子都是一个字典数据
    tmp = []

    for i in page_lst:
        # 判断是否超过阈值
        if int(i.find(class_='threadlist_rep_num').text) > M:
            dic = {}
            # 点击量
            dic['num'] = int(i.find(class_='threadlist_rep_num').text)
            # 帖子名称
            dic['name'] = i.find(class_='threadlist_title').text
            # 帖子地址
            dic['address'] = 'https://tieba.baidu.com' + i.find(class_='threadlist_title').a['href']

            tmp.append(dic)

    return tmp

# 爬取n页的数据
def search_n_pages(n):
    '''爬取n页数据'''
    target = []

    # 发起n次的get请求
    for i in range(n):
        # 跟踪进度
        print('page:', i)

        http=urllib3.PoolManager()         

        # 按照浏览贴吧的自然行为，每一页50条
        target_url = template_url.format(50*i)
        res = requests.get(target_url)

        # 转为 bs 对象
        soup = BeautifulSoup(res.text, 'html.parser')

        # 获取该页帖子列表
        page_lst = soup.find_all(class_='j_thread_list')

        # 该页信息保存到target
        target.extend(extra_from_one_page(page_lst))

        # 休息0.2秒再访问，友好型爬虫
        time.sleep(0.2)


    return target

name='原神'
head={'head':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

# get请求模版
template_url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(name,'{}')

# 爬取贴吧前200页数据
d = search_n_pages(10)

# 转化为pandas.DataFrame对象
data = pd.DataFrame(d)

# 导出到excel表格
data.to_excel('{}吧_{}.xlsx'.format(name,1))

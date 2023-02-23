import urllib3  
from urllib.parse import urlencode   
import json  
from urllib import parse
import requests
import cv2
from bs4 import BeautifulSoup as bs
from seleniumwire import webdriver

def url_imshow(urlcontent,headers=None):
    
    image=cv2.asarray(bytearray(urlcontent),dtype='uint8')
    cv2.imshow('i',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    
# with open(('user_h.json')) as fp:
#     head=json.load(fp)
# url='https://printidea.art/user/1546453'

# response =requests.request('GET',url,
#                            )
# data=response.content
# print(bs(data,features='lxml'))


with open(('user_h.json')) as fp:
    head=json.load(fp)
    
jdata=json.load(open('../datas/1.jpg','rb'))
url='https://printidea-img.oss-cn-hangzhou.aliyuncs.com/reference/pc/2023/01/17/1547284/1673942259697_90937b1a.jpg'

response =requests.request('PUT',url,
                           data=jdata
                           )
data=response.content
print(bs(data,features='lxml'))
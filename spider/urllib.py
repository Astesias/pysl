import urllib3  
from urllib.parse import urlencode   
import json  
from urllib import parse
import requests
from bs4 import BeautifulSoup as bs
from seleniumwire import webdriver
from pysl import easy_request

# urllib3.disable_warnings()    
        
# url='https://cg-api.heyfriday.cn/oss/getSTSToken'
# http=urllib3.PoolManager()              

# with open(('new_h.json')) as fp:
#     head=json.load(fp)

# response =http.request('GET',url,headers=head)
# data=response.data
# js=json.loads(data)
# print(js)


with open(('v3h.json')) as fp:
    head=json.load(fp)

payload={"inputText":"原","styleId":34,"artistId":10,"imageSizeId":1,"picUrl":"","multiple":2,"nid":1,"picRefType":1,"imageFactors":0.5,"reverseWords":"","modelId":1}

jdata=json.dumps(payload)

url= 'https://cg-api.heyfriday.cn/v1/generate/generateImageV3'
#    https://cg-api.heyfriday.cn/v1/generate/getGenerateDetails
# 'https://cg-api.heyfriday.cn/v1/generate/myPictureDetail?id=34402501'
# https://cg-api.heyfriday.cn/v1/generate/generateImageV3
# https://cg-api.heyfriday.cn/share/wxacodeV2
response =requests.request('POST',url,headers=head,
                            data=jdata
                            )
data=response.content
js=json.loads(data)
print(js)
batchNo=js['result']['batchNo']
id=js['result']['id']



with open(('new_h.json')) as fp:
    head=json.load(fp)


url= 'https://cg-api.heyfriday.cn/v1/generate/myPictureDetail?id={}'.format(id)
response =requests.request('GET',url,headers=head,
                            )
data=response.content
js=json.loads(data)
print(js['result']['pictureUrl'])

# print(easy_request(url='https://cg-api.heyfriday.cn/v1/generate/getGenerateDetails',
#                    header='v3h.json',
#                    ))


# 34383368
# 1547284
# batchNo=29e48c97b978455a8de3b978f2deb0ac
# https://m.printidea.art/pages/picture/generate?batchNo=29e48c97b978455a8de3b978f2deb0ac




















# from io import BytesIO
# import gzip

# buff = BytesIO(response.data)
# f = gzip.GzipFile(fileobj=buff)
# htmls = f.read().decode('utf-8')





# browser = webdriver.Chrome()
# browser.get(url)
# data = browser.page_source
# # 获取请求头信息
# try:
#     data=browser.requests
# finally:
#     browser.quit()
# # print(data)

# for re in data:
#     if '_headers' in dir(re.response) :
#         for h in re.response._headers:
#                 print(h)
            
        



# head={'head':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36','referer':'https://m.printidea.art/pages/picture/index?id=34381479','authorization':'eyJhbGciOiJIUzUxMiJ9.eyJwZXJtaXNzaW9uTGV2ZWwiOjEsInJlZnJlc2hDb3VudCI6MiwiaXNDaGVja1Bob25lIjowLCJ1c2VySWQiOjE4MzEzNCwiaWF0IjoxNjcyNTcxMzkzLCJleHAiOjE2NzMwODk3OTN9.jfma5zfxWoR-XTb188W62Wrzuo_kS0Tsg9wFnfhf5RdqNod250HKa8WfQdNsMzpsZWl-izkEohiA60KugsGg5A'}



# js=json.loads(response.data)

# print(response.)

# print('百度请求状态码：',get.status)
# print()


# url='https://www.httpbin.org/post'
# url='https://tieba.baidu.com/f?kw={}&ie=utf-8'.format(parse.quote('原神'))
# head={'head':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
# field={'country':'cn'}

# http2=urllib3.PoolManager()

# encoded_arg = urlencode(field)
# url = url + '?' + encoded_arg

# post=http2.request('POST',url,fields=field,headers=head,timeout=10)
# print('状态码：',post.status)

# data=json.loads(post.data.decode('unicode_escape')) 
# print('数据类型：',type(data))
# print('获取form对应的数据：',data.get('form'))
# print('获取country对应的数据：',data.get('form').get('country'))


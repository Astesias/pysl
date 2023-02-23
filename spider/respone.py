import urllib.request      #导入相应类库
import json  
import string
from pysl import isChinese

def issign(s):
    if s in '!,.':
        return 1
    else:
        return 0

url='https://tieba.baidu.com/p/8016648019'
url='https://iw233.cn/API/Random.php'
response = urllib.request.urlopen(url)
html = response.read()
print(html[:])
# with open('txt.txt','w') as fp:
#     fp.write(html.decode('utf-8','ignore').replace(u'\xa9', u'').replace(u'\U0001f34a', u''))
#     fp.close()

# with open('cn.txt','w') as fp:
#     last=''
#     for i in html.decode('utf-8','ignore').replace(u'\xa9', u'').replace(u'\U0001f34a', u''):
#         if (isChinese(i)):
#             fp.write(i)
#         # elif (isChinese(last)) and not (isChinese(i) or issign(i)):
#         #     fp.write('\n')
#         last=i
#     fp.close()
        
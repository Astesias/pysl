import requests
import re
import cv2
import numpy as np

# import sys
# t = sys.getfilesystemencoding()
# str.encode(xx).decode(t)
# import io
# sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


qq=2264168148
url=f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=100'
url=f'http://q.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640&img_type=jpg'
url_name=f'http://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={qq}'

html = requests.get(url_name)
# print(html.content)
s = html.content
print(html.encoding)


html = requests.get(url)
image = cv2.imdecode(np.asarray(bytearray(html.content),dtype='uint8'), cv2.IMREAD_COLOR)
cv2.imshow('',image)   
cv2.waitKey(0)

cv2.destroyAllWindows() 
# with open('qq.jpg','wb') as fp:
#     fp.write(html.content)

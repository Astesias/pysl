import requests
import random
import string
 
for num in range(20):
 	value = ''.join(random.sample(string.ascii_letters + string.digits, 8))
 	# 下载图片
 	url = "https://iw233.cn/API/Random.php"
    
 	r = requests.get(url)
 	# 写入图片
 	print("新增："+value)
 	with open('jpg/'+value+'.jpg', "wb") as f:
 	    f.write(r.content)


# u='https://paddle-imagenet-models-name.bj.bcebos.com/'
# r = requests.get(u)
# print(str(r.content,'utf8'))
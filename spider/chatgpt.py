import requests
import json
from urllib import parse
from bs4 import BeautifulSoup as bs

# print(parse.unquote('prompt=%E7%94%A8html%E5%86%99%E4%B8%80%E6%AE%B5%E6%98%BE%E7%A4%BA%E4%B8%80%E4%B8%AA%E6%A8%A1%E6%8B%9F%E6%97%B6%E9%92%9F%E7%9A%84%E4%BB%A3%E7%A0%81&openaiId=101527734469956768286371869843052352044700336730028'))

def chat(question):
    # qustion='用java实现它'
    url = 'http://chat.h2ai.cn/api/trilateral/openAi/completions?prompt={}&openaiId=101527734469956768286371869843052352044700336730028'.format(parse.quote(question))
    
    html= requests.request("GET", url,)
    soup=bs(html.text.replace('<br/>','#@$'),features="lxml")
    response=soup.find('body').text
    js=json.loads(response)
    return (js['data']['choices'][0]['text'].replace('#@$','\n'))


if __name__ == '__main__':  
    print(chat('your name '))
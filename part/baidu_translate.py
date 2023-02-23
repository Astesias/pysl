from bs4 import BeautifulSoup
from selenium import webdriver

def translate(txt):
    # txt=['翻译','中文','机器学习']
    if len(txt)>1:
        txtjoin='和'.join(txt)
    else:
        txtjoin=txt[0]
    url=f'https://fanyi.baidu.com/#zh/en/{txtjoin}'
    
    browser = webdriver.Chrome()
    browser.get(url)
    data = browser.page_source
    browser.quit()
    
    soup=BeautifulSoup(data,'lxml')
    output=soup.find_all(id="original-output",style="display:none;")[0]
    result=output.getText()
    if len(txt)>1 and 'and' in result:
        result=result.split('and')
    if type(result)==type(''):
        result=[result]
    
    rs=[]
    for i in range(len(txt)):
        r=result[i].strip(' ')
        # print(f'{txt[i]} -> {r}')
        rs.append(r)
        
    # Genshin Impact
    # </div><div style="display:none;" id="original-output"><p>Genshin Impact</p></div></body></html>
    return rs

if __name__ == '__main__':
    print(*translate(['百度','翻译']))
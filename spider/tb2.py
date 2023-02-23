from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import codecs
from urllib import parse
import time


class tiebaSpider(object):
    def __init__(self, base_url, maxPage):
        self.headers = {'User-Agent': UserAgent().random if 0 else 'Baiduspider',
                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",}
        self.i = 0
        self.main(base_url, maxPage)

    def getPageHtml(self, url):
        try:
            req = requests.get(url, headers=self.headers)
            req.encoding = 'utf-8'
            html = req.text
            html = html.replace(r'<!--', '"').replace(r'-->', '"')
            return html
        except:
            print("获取page失败！")

    def get_Info(self, html):
        informations = []  # 存放所有信息的列表
        soup = BeautifulSoup(html, 'lxml')
        li_tags = soup.find_all('li', class_="j_thread_list clearfix thread_item_box")
        for li in li_tags:  # 遍历找到的li标签,一个li标签代表一个帖
            info = {}  # 用字典存储获取的信息
            try:
                info['title'] = li.find(
                    'div', class_="threadlist_abs threadlist_abs_onlyline"
                ).text.strip()

                info['link'] = "https://tieba.baidu.com" + \
                               li.find('a', class_='j_th_tit')['href']

                info['author'] = li.find('span', class_='tb_icon_author')['title']

                info['time'] = li.find(
                    'span', class_='pull-right is_show_create_time'
                ).text.strip()

                info['replyNum'] = li.find(
                    'span', class_='threadlist_rep_num center_text'
                ).text.strip()

                informations.append(info)
            except:
                print("从标签中取信息出了问题！")
        print(len(informations))
        return informations

    def writeInfo(self, infoList):  # 写入TXT文件中
        with codecs.open(r'{}吧帖子爬取.txt'.format(name), 'a+', 'utf-8') as f:
            for info in infoList:
                f.write(
                    "标题：{}\t链接：{}\t帖子作者：{}\t发帖时间：{}\t回帖数量：{}\n\n".format(
                        info['title'], info['link'], info['author'], info['time'], info['replyNum']
                    )
                )
        self.i += 1
        print("第%d页打印完成！" % self.i)

    def main(self, base_url, maxPage):
        for p in range(0, maxPage):
            time.sleep(0.2)
            url = base_url + str(p * 50)
            self.html = self.getPageHtml(url)
            self.imfoList = self.get_Info(self.html)
            self.writeInfo(self.imfoList)


if __name__ == '__main__':
    
    name='原神内鬼'
    base_url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=".format(parse.quote(name))
    T=tiebaSpider(base_url, 10)

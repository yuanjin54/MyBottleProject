from lxml import etree
import requests
import re
from bs4 import BeautifulSoup


class Spider(object):
    """
    从百度知道爬取问题答案
    """

    def __init__(self):
        self._url_1 = "https://zhidao.baidu.com/search?word="
        self._url_2 = "&ie=gbk&site=-1&sites=0&date=0&pn="
        self._headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                       'Chrome/60.0.3112.78 Safari/537.36'}

    def search_qs(self, question: str, top=3):
        """
        输入问题，通过爬虫爬去百度知道问题对和答案
        :param question:
        :return: List[(question, answer)]
        """
        res = []
        try:
            html, number = self.get_html(question)
            urls = self.get_url(html)
            for u in urls[:top]:
                ask, answer = self.get_info(u)
                if len(ask.strip()) == 0 or len(answer.strip()) == 0:
                    continue
                res.append((ask, answer))
        except Exception as e:
            print(e)
        return res

    def get_html(self, keyword, number=0):
        # 输入关键字，获取得到结果的数量和源码
        # 如果是首页，返回首页的HTML源码和最大页数；如果不是，则只返回HTML源码

        url = self._url_1 + keyword + self._url_2 + str(number)
        # print(url)
        res = requests.get(url=url, headers=self._headers)
        res.encoding = 'gbk'
        html = res.text
        if number == 0:
            reg = r'<a class="pager-last".+?pn=(.+?)">尾页</a>'
            reg = re.compile(reg)
            number = re.findall(reg, html)[0]
            return html, number
        else:
            return html

    def get_url(self, html):
        # 从html源码中解析出url并返回
        Soup = BeautifulSoup(html, 'lxml')
        info = Soup.select('.list-inner')
        info = info[0].select('.ti')
        return [i['href'] for i in info]

    def get_info(self, url):
        # 传入详情页的URL，进入详情页获取问题和答案并返回
        title_xpath = '//*[@id="wgt-ask"]/h1/span'
        answer_xpath = '//div[@accuse="aContent"]'
        res = requests.get(url, headers=self._headers)
        res.encoding = 'gbk'
        #     print(res.text)
        page = etree.HTML(res.text)
        # 详情页的问题和答案一共有三种情况，一是普通问题，二是作业帮的问答问题，三是丢失的问答
        ask = ''
        info = ''
        try:
            title_element = page.xpath(title_xpath)
            if len(title_element) > 0:
                ask = title_element[0].text
        except Exception as e:
            ask = ''
            print(str(e))
            print('获取问题失败,对应的URL为:', url)
        try:
            infos = []
            answer_elements = page.xpath(answer_xpath)
            for ans in answer_elements[0]:
                if ans.tag == 'p':
                    if ans.text is None:
                        continue
                    else:
                        infos.append(ans.text.strip())
                elif ans.tail is not None and len(ans.tail.strip()) > 0:
                    infos.append(ans.tail.strip())
            info = ''.join(infos)
        except Exception as e:
            print(str(e))
            info = ''
            print('获取标题失败，对应的URL为:', url)
        return ask, info


if __name__ == '__main__':
    spd = Spider()
    question = '中国有多大'
    ans = spd.search_qs(question)
    print(ans)

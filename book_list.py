import re

from urllib import request

class BookList():
    '''
    建立一个类单独获取书名与书籍详细信息的URL
    '''
    root_pattern = '<div class="pl2">([\s\S]*?)</a>'
    href_pattern = 'href="([\s\S]*?)"'
    name_pattern = 'title="([\s\S]*?)"'

    def __get_url(self,count):
        url = 'https://book.douban.com/top250?start='+count
        return url

    def __fetch_content(self):
        a = range(0,250,25)
        htmls = ''
        for i in list(a):
            url = self.__get_url(str(i))
            r = request.urlopen(url)
            html = r.read()
            html = str(html,encoding='utf-8')
            htmls += html
        return htmls

    def __analysis(self,htmls):
        root_html = re.findall(BookList.root_pattern,htmls)
        anchors = []
        for html in root_html:
            name = re.findall(BookList.name_pattern,html)
            href_html = re.findall(BookList.href_pattern,html)
            anchor = {'name':name,'href':href_html}
            anchors.append(anchor)
        return anchors

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        return anchors
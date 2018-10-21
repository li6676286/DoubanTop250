import re

from urllib import request
from book_list import BookList

class BookMessage():
    '''
    根据之前获取的URL爬取书籍剩余的详细信息
    '''
    root_pattern = '<div id="info"[\s\S]*?>([\s\S]*?)</div>'
    detail_pattern = '<span class="pl">(.*?)</span>([\s\S]*?)<br'
    contents_pattern = 'href="[\s\S]*?">([\s\S]*?)</a>'
    n_pattern = '<div class="intro">([\s\S]*?)</div>'
    get_content_pattern = '<p>([\s\S]*?)</p>'

    def __fetch_content(self,url):
        r = request.urlopen(url)
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        return htmls

    def __analysis(self,htmls):
        root_html = re.findall(BookMessage.root_pattern,htmls)
        detail_html = re.findall(BookMessage.detail_pattern,root_html[0])
        n_html = re.findall(BookMessage.n_pattern,htmls)
        contents = re.findall(BookMessage.get_content_pattern,n_html[0])
        anchors = []
        content_str = ''
        for i in detail_html:
            name = i[0]
            msg = i[1]
            if 'href' in msg :
                msg1 = re.findall(BookMessage.contents_pattern,msg)
                di = {name:msg1[0].strip()}
            else :
                msg.strip()
                di = {name:msg}
            anchors.append(di)
        for i in contents:
            content_str+=i
        dc = {'内容简介:':content_str}
        anchors.append(dc)
        return anchors

    def __refine(self,anchors):
        for i in anchors:
            for key in i.keys():
                print(key+i.get(key))
            
    def go(self):
        booklist = BookList()
        book = booklist.go()
        for i in book:
            try:
                htmls = self.__fetch_content(i['href'][0])
                anchors = self.__analysis(htmls)
                print('书名:'+i['name'][0])
                self.__refine(anchors)
            except Exception:
                print('书籍信息有误,连接出现异常')
            continue

bookmsg = BookMessage()
bookmsg.go()
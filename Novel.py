import requests
import os
from pyquery import PyQuery as pq
from multiprocessing.pool import Pool


def down(url):
    '''
    下载网页内容
    :param:url:网页链接地址
    :return:response.text:返回响应内容
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    if url:
        try:
            response = requests.get(url,headers=headers)
            response.encoding = response.apparent_encoding
            return response.text
        except:
            return None

def parse_content(html):
    '''
    解析最终章节内容
    :param:html:响应内容
    :return:title/ctn:章节标题、内容
    '''
    try:
        if html != None:
            doc = pq(html)
            ttl = doc('h2').text()
            ctn = doc('#inner').text()
            print(ttl,end=' ')
            return ttl , ctn
    except:
        print('解析最终章节内容出错πππππππ')
def save(fp,text):
    '''
    保存最终小说内容
    :param fp: 保存路径
    :param text: 最终内容
    :return: None
    '''
    try:

        with open(fp, 'a', encoding='utf-8') as f:
            f.write(text)
            print(fp, '保存成功')
    except:
        print(fp, '出错啦')
def one_chapter(name,url):
    '''
    下载一个章节内容
    :param:url:章节链接
    '''
    html = down(url)
    ttl, text = parse_content(html)
    if not os.path.exists('小说'):
        os.mkdir('小说')
    name = name + r'.txt'
    fp = '小说' + '/' + name
    save(fp, ttl + '\n\n' + text + '\n\n')

def parse_chapter_links(html):
    '''
    解析章节链接
    :param:html:章节索引页面
    :return:links:返回解析出来的章节链接
    '''
    doc = pq(html)
    links = list(doc('div.dir_main_section ol li a').items())
    return links

def Chapter_links(url):
    '''
    获取所有章节链接
    :param:url:每本小说的链接
    :return:所有章节链接
    '''
    # url = 'http://www.cuiweiju888.com/6/6553/index.html'
    chapterslink = []
    html = down(url)
    links = parse_chapter_links(html)
    for link in links:
        chapterslink.append('http://www.cuiweiju888.com' + link.attr.href)
    return chapterslink

def parse_and_get_all_novels(html):
    '''
    解析并获得所有的小说链接
    :param html: 包含小说链接的网页
    :return: 小说名字和小说链接
    '''
    novelDict = {}
    doc = pq(html)
    a = doc('ul.bd li p a')
    for i in a:
        novelName = i.text
        novelLink = i.attrib['href']
        novelId = novelLink.split('/')[-1].split('.')[0]
        novelDict[novelName] = novelId
    return novelDict

def structure_urls():
    urls = []
    for i in range(1,3):
        url = 'http://www.cuiweiju888.com/list1_%d.html'%i
        urls.append(url)
    return urls

def all_novels(url):
    '''
    所有的玄幻小说
    :return:
    '''
    novelsIndex = []
    html = down(url)
    novelDict = parse_and_get_all_novels(html)
    for k in novelDict:
        novelIndex = r'http://www.cuiweiju888.com/5/%s/index.html'%novelDict[k]
        novelDict[k] = novelIndex
    return novelDict

def main(url):
    novelDict = all_novels(url)
    for name in novelDict:
        chapterslink = Chapter_links(novelDict[name])
        for eachChapter in chapterslink:
            one_chapter(name,eachChapter)

if __name__ == '__main__':
    urls = structure_urls()
    # for i in urls:
    #     print(i)
    #     main(i)
    pool = Pool()
    pool.map(main,urls)
    pool.close()
    pool.join()

import requests
from lxml import etree
from urllib.parse import urljoin
from time import sleep
import os

#获得请求头
def head(i):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 't1.onvshen.com:85',
        'If-Modified-Since': 'Sun, 25 Mar 2018 01:41:11 GMT',
        'If-None-Match': "f872e65adac3d31:0",
        'Referer': i,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    return headers

#解析30个图集页面，得到每个图集地址
def parse_gallery_url(gallery_url):
    response = etree.HTML(requests.get(gallery_url).text)
    gallery_urls = response.xpath('//*[@id="listdiv"]/ul/li/div[1]/a/@href')
    for url in gallery_urls:
        yield 'https://www.nvshens.com' + url

def get_title(album_url):
    response = etree.HTML(requests.get(album_url).text)
    title = response.xpath('//*[@id="htilte"]/text()')[0]
    os.mkdir('D:\\图片\\'+title)
    return title


#得到图片名称、每一页地址
def get_pictures_url(url):
    response = etree.HTML(requests.get(url).text)
    page_href = response.xpath('//div[@id="pages"]/a/@href')[:-2]
    for href in page_href:
        yield urljoin(url, href)

#获取所有图片的链接
def get_per_picture_page(url):
    response = etree.HTML(requests.get(url).text)
    pictures_url = response.xpath('//*[@id="hgallery"]/img/@src')
    return pictures_url
#下载图片
def download(picture_url, url, filename):
    response = requests.get(picture_url, headers=head(url)).content
    picture_name = picture_url.split('/')[-1]
    with open('D:\\图片\\{}\\'.format(filename) + picture_name , 'wb') as file:
        file.write(response)

#设置开始和结束的页面
def start_stop(start):
    gallery_url = 'https://www.nvshens.com/gallery/'
    if start == 1:
        return gallery_url
    else:
        gallery_url = 'https://www.nvshens.com/gallery/{}.html'.format(start)
        return gallery_url

#解析所有链接、页面
def parse():

    for album_url in parse_gallery_url(start_stop(num)):#遍历每个album
        try:
            filename = get_title(album_url)
            for url in get_pictures_url(album_url): #遍历album的每一页
                for picture_url in get_per_picture_page(url):
                    download(picture_url, url, filename)
            sleep(3)
        except:
            print(album_url)
            pass

if __name__ == '__main__':
    start = int(input('请输入开始的页数：'))
    stop = int(input('请输入结束的页数：'))
    for num in range(start, stop+1):
        parse()




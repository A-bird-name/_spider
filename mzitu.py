import requests
from lxml import etree
import os
from time import sleep

def head(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'i.meizitu.net',
        'If-Modified-Since': 'Fri, 30 Mar 2018 02:50:57 GMT',
        'If-None-Match': '"5abda611-13686"',
        'Referer': url,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    return headers


def gallery_url(num):
    if num == 1:
        gallery_url = 'http://www.mzitu.com'
    else:
        gallery_url = 'http://www.mzitu.com' + '/page/{}/'.format(num)
    return gallery_url

def get_album_url(gallery_url):
    response = etree.HTML(requests.get(gallery_url).text)
    album_urls = response.xpath('//ul[@id="pins"]/li/a/@href')
    for album_url in album_urls:
        yield album_url

def get_all_album_pages_url(album_url):
    response = etree.HTML(requests.get(album_url).text)
    num_of_pages = response.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    num_of_pages = int(num_of_pages)  #取得一个album的总页数
    for i in range(1, num_of_pages+1):
        if i == 1:
            album_page_url = album_url
        else:
            album_page_url = album_url + '/{}'.format(i)
        yield album_page_url


def get_per_picture_url(album_page_url):
    response = etree.HTML(requests.get(album_page_url).text)
    picture_url = response.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
    return picture_url

def downloads(picture_url, album_page_url, filename):
    response = requests.get(picture_url, headers=head(album_page_url)).content
    picture_name = picture_url.split('/')[-1]
    with open('D:\\图片\\{}\\'.format(filename) + filename + picture_name, 'wb') as file:
        file.write(response)

def get_title(album_url):
    response = etree.HTML(requests.get(album_url).text)
    title = response.xpath('//h2/text()')[0]
    os.mkdir('D:\\图片\\'+title)
    return title


def parse(start, stop):
    for num in range(start, stop+1):
        for album_url in get_album_url(gallery_url(num)):
            filename = get_title(album_url)
            for album_page_url in get_all_album_pages_url(album_url):
                picture_url = get_per_picture_url(album_page_url)
                downloads(picture_url, album_page_url, filename)
        sleep(1)
if __name__ == '__main__':
    start = int(input("请输入从那一页开始："))
    stop = int(input("请输入在那一页结束："))
    parse(start, stop)
# -*- coding:utf-8 -*-

import urllib
import urllib2
from lxml import etree

def loadPage(url):
    """
        作用：根据url发送请求，获取服务器响应文件
        url：需要爬取的url地址
    """
    request = urllib2.Request(url)
    html = urllib2.urlopen(request).read()
    #解析HTML文档为html dom模型
    content = etree.HTML(html)

    link_list = content.xpath('//div[@class="t_con cleafix"]/div//div/div/a/@href')
    #返回所有匹配成功的列表集合
    for link in link_list:
        #每个帖子的链接
        fullink = "https://tieba.baidu.com" + link
        loadImage(fullink)

def loadImage(fullink):
    #作用：取出每个帖子里的每个图片链接
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    request = urllib2.Request(fullink, headers = headers)
    html = urllib2.urlopen(request).read()
    content =etree.HTML(html)
    #取出贴子里的所有图片集合
    link_list = content.xpath('//div/img[@class="BDE_Image"]/@src')
    #取出每个图片的链接
    for link in link_list:
        #print link
        writeImage(link)
def writeImage(link):
    """
        作用：将image图片写入到本地
        link：图片链接
    :param link:
    :return:
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    #文件写入
    request = urllib2.Request(link, headers=headers)
    #图片原始数据
    image = urllib2.urlopen(request).read()
    #取出链接后十位作为图片名
    filename = link[-10:]
    #写入到本地磁盘文件内
    with open(filename, "wb") as f:
        f.write(image)

def tiebaSpider(url, beginPage, endPage):
    """
    #作用：贴吧爬虫调度器，负责组合处理每个页面的url请求
    url ： 贴吧url的前部分
    beginPage： 起始页
    endPage： 结束页
    :param url:
    :param beginPage:
    :param endPage:
    :return:
    """
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        fullurl = url + "&pn=" + str(pn)
        loadPage(fullurl)

if __name__ == "__main__":
    kw = raw_input("请输入需要爬取的贴吧名：")
    beginPage = int(raw_input("请输入起始页:"))
    endPage = int(raw_input("请输入结束页:"))
    url = "http://tieba.baidu.com/f?"
    key = urllib.urlencode({"kw":kw})
    fullurl = url + key
    tiebaSpider(fullurl, beginPage, endPage)
# -*- coding:utf-8 -*-
import urllib
import urllib2
import lxml.html as HTML
import pandas
import requests

#get HTML
url = 'http://dxy.com/column/special/153/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
headers = {'User-Agent': user_agent}

request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)

# Analyze
content = response.read()
content = content.decode('utf-8')
htmlSource = HTML.fromstring(content)

itemurl = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dt/a/@href')
# itemcontent = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dd/div/text()')
# itemtheme = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dd/div[@class="hd-tit"]/h4[@class="hd"]/a/text()')
# author = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dd/div[@class="hd-tit"]/div[@class="author"]/a/text()')

# compensate incompleted url
for i in range(len(itemurl)):
	itemurl[i] = 'http://dxy.com' + itemurl[i] + '/'

totalTag = []
totalAuthor = []
totalContent = []
totalTime = []
totalTopic = []
#爬取文档下的内容
for singleUrl in itemurl:
	request = urllib2.Request(singleUrl, headers=headers)
	response = urllib2.urlopen(request)
	content = response.read()
	content = content.decode('utf-8')
	htmlSource = HTML.fromstring(content)
	#爬取作者
	singleAuthor = htmlSource.xpath('//p[@class="info"]/span[@class = "author"]/a/text()')
	totalAuthor.append(singleAuthor)
	#爬取标签
	singleTag =  htmlSource.xpath('//div[@class="mod-tag mt50 J-col-tag"]/a/text()')
	totalTag.append(singleTag)
	#爬取时间
	singleTime = htmlSource.xpath('//p[@class="info"]/span[@class = "time"]/text()')
	totalTime.append(singleTime)
	#爬取主题
	singleTopic = htmlSource.xpath('//div[@class="pg-article-hd"]/h1/text()')
	totalTopic.append(singleTopic)
	#爬取文章内容
	singleContent = htmlSource.xpath('//div[@class="editor-body"]/p/text()|//div[@class="editor-body"]/div/text()|//div[@class="editor-body"]/p/font/font/text()')
	totalContent.append(singleContent)

item = [totalTopic,totalTime,totalAuthor,totalTag,totalContent]
#矩阵转置
item = map(list ,zip(*item))

#output csv file
paper = pandas.DataFrame(item)
paper.to_csv("153.csv",encoding='GB18030',header=False,index=False,mode='a')


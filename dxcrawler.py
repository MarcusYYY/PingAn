# -*- coding:utf-8 -*-
import urllib
import urllib2
import lxml.html as HTML
import pandas
import requests

#get HTML
url = 'http://dxy.com/column/special/224/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
headers = {'User-Agent': user_agent}

request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)

# Analyze
content = response.read()
content = content.decode('utf-8')
htmlSource = HTML.fromstring(content)

itemurl = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dt/a/@href')
itemcontent = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dd/div/text()')
itemtheme = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dd/div[@class="hd-tit"]/h4[@class="hd"]/a/text()')
author = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dd/div[@class="hd-tit"]/div[@class="author"]/a/text()')

# compensate incomplete url
for i in range(len(itemurl)):
	itemurl[i] = 'http://dxy.com' + itemurl[i] + '/'

totalTag = []

#get tags of each item
for singleUrl in itemurl:
	request = urllib2.Request(singleUrl, headers=headers)
	response = urllib2.urlopen(request)
	content = response.read()
	content = content.decode('utf-8')
	htmlSource = HTML.fromstring(content)
	singleTag =  htmlSource.xpath('//div[@class="mod-tag mt50 J-col-tag"]/a/text()')
	totalTag.append(singleTag)

item = [itemurl,itemtheme,author,totalTag,itemcontent]
item = map(list ,zip(*item))

#output csv file
paper = pandas.DataFrame(item)
paper.to_csv("attempt.csv",encoding='GB18030',header=False,index=False,mode='a')


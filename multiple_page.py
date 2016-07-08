# -*- coding: utf-8 -*-
_author_ = 'Marcus'

import urllib2
import lxml.html as HTML
import pandas
from _single_page import *
# import requests
# import csv
# import string

# 得到网站的HTML源代码
def getPage(url, encoding):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    source = HTML.fromstring(response.read().decode(encoding))
    return source

# 写入csv文件中
def WriteToCSV(csvName, text, zp):
	if zp == 0:
		title = [("症状名称","症状链接","症状简述","症状起因","可能疾病","诊断详述","对症药品","常见检查","相似症状")]
		title = pandas.DataFrame(title)
		title.to_csv(csvName, encoding='utf-8', header=False, index=False, mode='a')
	paper = pandas.DataFrame(text)
	paper.to_csv(csvName, encoding='utf-8', header=False, index=False, mode='a')

# 获取下一页的URL
def getNextPageURL(source):
    nextPage = source.xpath('//div[@id ="res_subtab_1"]/div[@class="site-pages"]/a[@class="sp-a"]/text()')
    nextPageURL = source.xpath('//div[@id ="res_subtab_1"]/div[@class="site-pages"]/a[@class="sp-a"]/@href')
    temp = 0
    for p in nextPage:
        if p == u'下页':
            return nextPageURL[temp]
        temp = temp + 1

# 得到该页所有疾病的疾病名称
def getName(source):
    diseaseName = source.xpath('//div[@class="res_list"]/dl/dt[@class="clearfix"]/h3/a/text()')
    return diseaseName

# 得到该页所有疾病的症状URL
def getdiseaseURL(source):
    url = []
    diseaseUrl = source.xpath('//div[@class="res_list"]/dl/dt[@class="clearfix"]/h3/a/@href')
    for i in range(0, len(diseaseUrl)):
        url.append(diseaseUrl[i])
    return url







"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""
total = [('疾病', '症状链接')]
WriteToCSV('mainPage\mainURL_001-100.csv', total)
WriteToCSV('mainPage\mainURL_101-200.csv', total)
WriteToCSV('mainPage\mainURL_201-300.csv', total)
WriteToCSV('mainPage\mainURL_301-400.csv', total)
WriteToCSV('mainPage\mainURL_401-500.csv', total)
WriteToCSV('mainPage\mainURL_501-600.csv', total)
WriteToCSV('mainPage\mainURL_601-700.csv', total)
WriteToCSV('mainPage\mainURL_701-000.csv', total)
"""

urlTemp = '/bw_t2_p1#ps'

temp = 1
while urlTemp != None:

	url = 'http://jbk.39.net' + urlTemp
	print '-------------------------------------------'
	print 'temp' + str(temp) + ':' + url
	temp = temp + 1


	#get the HTML source code of the current page
	source = getPage(url, 'GB18030')

	#name of disease
	diseaseName = getName(source)

	#get all links of current diseases
	blbyUrl = getdiseaseURL(source)

	for zp in range(0, len(diseaseName),1):
		title = diseaseName[zp]
		Singleurl = blbyUrl[zp]
		info = getInfo(title,Singleurl)
		if temp <= 100:
			WriteToCSV('mainPage\mainURL_001-100.csv', info ,zp)
		elif temp <= 200 and temp > 100:
			WriteToCSV('mainPage\mainURL_101-200.csv', info ,zp)
		elif temp <= 300 and temp > 200:
			WriteToCSV('mainPage\mainURL_201-300.csv', info ,zp)
		elif temp <= 400 and temp > 300:
			WriteToCSV('mainPage\mainURL_301-400.csv', info ,zp)
		elif temp <= 500 and temp > 400:
			WriteToCSV('mainPage\mainURL_401-500.csv', info ,zp)
		elif temp <= 600 and temp > 500:
			WriteToCSV('mainPage\mainURL_501-600.csv', info ,zp)
		else:
			 WriteToCSV('mainPage\mainURL_601-700.csv',info ,zp)
	urlTemp = getNextPageURL(source)

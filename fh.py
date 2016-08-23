# -*- coding:utf-8 -*-
"""
飞华健康网
"""
__author__ = 'Marcus'
import urllib2
import lxml.html as HTML
import pandas
import numpy
import re
import time

#模仿浏览器登录网站
def getPage(url, encoding):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    request = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(request)
    except Exception,e:
        print Exception,";",e
        return None
    try:
        source = HTML.fromstring(response.read().decode(encoding,'ignore'))
    except Exception,e:
        print Exception,";1000",e
        return None
    return source

# 写入csv文件中
def WriteToCSV(csvName,text):
	paper = pandas.DataFrame(text)
	paper.to_csv(csvName, encoding='GB18030', header=False, index=False, mode='a')


"""------------------------------------main--------------------------------------"""
"""------------------------------------main--------------------------------------"""
"""------------------------------------main--------------------------------------"""

#从主网页进入
main_Page = "http://ys.fh21.com.cn/sport/list_144"
main_source = getPage(main_Page + '.html','GB18030')

Page_Pool = ['_1','_2','_3','_4','_5','_6','_7']
csvName = u'飞华养身' + '.csv'
title = [("文章名称","链接","内容","标签")]
title = pandas.DataFrame(title)
title.to_csv(csvName,encoding='GB18030', header=False, index=False,mode='a')


for singlePage in Page_Pool:
	current_page = main_Page + singlePage + '.html'
	source = getPage(current_page,'GB18030')
	articlePool = source.xpath('//div[@class="catalog04"]/ul/p/a/@href')
	UrlPool = []

	for everyURL in articlePool:
		everyURL= 'http://ys.fh21.com.cn' + everyURL
		UrlPool.append(everyURL)
	titlePool = source.xpath('//div[@class="catalog04"]/ul/p/a/text()')
	
	for idx in range(0,len(UrlPool)):
		print UrlPool[idx],idx
		print '-----------------------------------------------'
		detail_source = getPage(UrlPool[idx],'GB18030')
		detail = []
		next_page = detail_source.xpath('//ul[@class="pageStyle"]/li[last()]/a/@href')
		tag = detail_source.xpath('//div[@class="detail03b"]/a/text()')
		tag = ','.join(tag)
		if next_page:
			next_page = 'http://ys.fh21.com.cn/sport/' + next_page[0]
			while 1:
				content = detail_source.xpath('//div[@class="detailc"]/p/text()')
				content = ''.join(content)
				detail.extend(content)
				page = detail_source.xpath('//ul[@class="pageStyle"]/li[last()]/a/@href')
				if page:
					next_page = 'http://ys.fh21.com.cn/sport/' + page[0]
					if page[0] == 'javascript:void(0);':
						break
					detail_source = getPage(next_page,'GB18030')
		else:
			content = detail_source.xpath('//div[@class="detailc"]/p/text()')
			content = ''.join(content)
			detail.extend(content)

		detail = ''.join(detail).replace('\n','').replace('\r','')
		item = [(titlePool[idx],UrlPool[idx],detail,tag)]
		WriteToCSV(csvName,item)






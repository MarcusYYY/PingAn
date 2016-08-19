# -*- coding:utf-8 -*-
"""
寻医问药运动栏
"""


__author__ = 'Marcus'
import urllib2
import lxml.html as HTML
import pandas
import numpy
import re
import time

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
def WriteToCSV(csvName,text,index,idx):
	if index%100 == 0 and idx == 0:
		title = [("文章名称","链接","内容")]
		title = pandas.DataFrame(title)
		title.to_csv(csvName,encoding='GB18030', header=False, index=False,mode='a')
	paper = pandas.DataFrame(text)
	paper.to_csv(csvName, encoding='GB18030', header=False, index=False, mode='a')


"""------------------------------------main---------------------------------------------------"""
"""------------------------------------main---------------------------------------------------"""
"""------------------------------------main---------------------------------------------------"""


main_Page = "http://jianfei.xywy.com/yundong/"
main_source = getPage(main_Page,'GB18030')
next_Page = main_source.xpath('//div[@class="page tc ant-s14"]/ul/li[last()-1]/a/@href')


for index in range(,262):
	csvName = 'sport' + str(index/100) + '00_.csv' 
	url = main_source.xpath('//div[@class="article-list-box"]/ul/li/div/h3/a/@href')
	title = main_source.xpath('//div[@class="article-list-box"]/ul/li/div/h3/a/text()')
	for idx in range(0,len(url)):
		print url[idx],index,idx
		print '--------------------------------------------------'
		# time.sleep(0.5)
		detail_source = getPage(url[idx],'gbk')
		if detail_source == None:
			continue
		text = detail_source.xpath('//div[@class="d-art-sec"]/p/text()|//div[@class="d-art-sec"]/p/strong/text()|//divstyle/strong/text()|//divstyle/text()')
		text = ''.join(text)
		item = [(title[idx],url[idx],text)]
		WriteToCSV(csvName,item,index,idx)
	main_Page = next_Page[0]
	main_source = getPage(main_Page,'gb2312')
	next_Page = main_source.xpath('//div[@class="page tc ant-s14"]/ul/li[last()-1]/a/@href')
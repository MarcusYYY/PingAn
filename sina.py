# -*- coding:utf-8 -*-
"""
Diseases
"""
__author__ = 'Marcus'

import urllib2
import lxml.html as HTML
import pandas
import numpy
import re


def getPage(url, encoding):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    request = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(request)
    except Exception,e:
        print Exception,";",e
        return None
    # response = urllib2.urlopen(request)
    try:
        source = HTML.fromstring(response.read().decode(encoding))
    except Exception,e:
        print Exception,";",e
        return None
    return source

# 写入csv文件中
def WriteToCSV(csvName, text):
    paper = pandas.DataFrame(text)
    paper.to_csv(csvName, encoding='GB18030', header=False, index=False, mode='a')

def DealWithTitle(title):
	title = ''.join(title)
	title = title.encode('utf-8')
	title = title.split("：")
	title = title[1:]
	title = ''.join(title)
	return title

def DealWithContent(content):
	content = ''.join(content)
	content = content.encode('utf-8')
	return content



"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""

main_url = "http://health.sina.com.cn/disease/department/knx/"
main_page = getPage(main_url,'utf-8')
print main_page
department_id = ["","1","2","4","6","7","8"]
department_url = []
department_name = []

writeCSV = u'新浪疾病_' + '.csv'
title = [("疾病名称","所属部位","就诊科室","症状体征","病因","症状","检查","预防","治疗")]
title = pandas.DataFrame(title)
title.to_csv(writeCSV,encoding='GB18030', header=False, index=False,mode='a')

for num in department_id:
	_url = '//div[@id="test' + num + '-content"]/ul/li/a/@href'
	_name = '//div[@id="test' + num + '-content"]/ul/li/a/text()'
	_page = main_page.xpath(_url)
	name_ = main_page.xpath(_name)
	name_ = ''.join(name_)
	name_ = name_.encode('utf-8')
	department_url.extend(_page)
	department_name.append(name_)



for each_url in  department_url:
	disease_url = getPage(each_url,'utf-8')
	if disease_url == None:
		continue
	disease_ = disease_url.xpath('//div[@class="main_R1_txt"]/ul/li/a/@href')
	disease_name = disease_url.xpath('//div[@class="main_R1_txt"]/ul/li/a/text()')
	information = []
	for detail in disease_:
		index = 0
		print '-------------------------------'
		print detail
		item = ['bingyin.html','zhengzhuang.html','jiancha.html','yufang.html','zhiliao.html']
		name = ''
		part = ''
		department = ''
		trait = ''
		symptom = ''
		reason = ''
		heal = ''
		check = ''
		prevent = ''
		for content in item:
			url_ = detail + content
			source = getPage(url_,'GB18030')
			if source == None:
				continue
			if content == 'bingyin.html':
				name = source.xpath('//div[@class="box_txt"]/ul/li[1]/text()')
				part = source.xpath('//div[@class="box_txt"]/ul/li[2]/text()')
				department = source.xpath('//div[@class="box_txt"]/ul/li[3]/text()')
				trait = source.xpath('//div[@class="box_txt"]/ul/li[4]/text()')
				reason = source.xpath('//div[@class="txt_xx"]/p/text()')
				name = DealWithTitle(name)
				part = DealWithTitle(part)
				department = DealWithTitle(department)
				trait = DealWithTitle(trait)
				reason = DealWithContent(reason)

			elif content == 'zhengzhuang.html':
				symptom = source.xpath('//div[@class="txt_xx"]/p/text()')
				symptom = DealWithContent(symptom)

			elif content == 'jiancha.html':
				check = source.xpath('//div[@class="txt_xx"]/p/text()')
				check = DealWithContent(check)

			elif content == 'yufang.html':
				prevent = source.xpath('//div[@class="txt_xx"]/p/text()')
				prevent = DealWithContent(prevent)

			else:
				heal = source.xpath('//div[@class="txt_xx"]/p/text()')
				heal = DealWithContent(heal)
		result = (name,part,department,trait,reason,symptom,check,prevent,heal)
		information.append(result)
	WriteToCSV(writeCSV,information)
	

			





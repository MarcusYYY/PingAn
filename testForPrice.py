# -*- coding:utf-8 -*-
"""
常用药品
"""

__author__ = 'Marcus'

import urllib2
import lxml.html as HTML
import pandas
import numpy
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time

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
def WriteToCSV(csvName,text,temp):
    if temp == 0:
        title = [("疾病名称","诊疗医院","最低价格","最高价格")]
        title = pandas.DataFrame(title)
        title.to_csv(csvName,encoding='GB18030', header=False, index=False,mode='a')
    paper = pandas.DataFrame(text)
    paper.to_csv(csvName, encoding='GB18030', header=False, index=False, mode='a')

#Find the lowbound and highbound of price
def DealWithPrice(Original):
	
	bottle = []
	lowbound = 0
	highbound = 0
	
	if len(Original) == 1:
		words = Original[0]
	else:
		words = Original[1]	
	words = words.replace('\n','').replace('\r','').replace(' ','')
	for word in words:
		try:
			word = int(word)
			bottle.append(word)
		except:
			continue
	for num in bottle:
		if lowbound == 0 and num != 0 and highbound == 0:
			lowbound = num
		elif lowbound != 0 and num == 0 and highbound == 0:
			lowbound = lowbound * 10 + num
		elif lowbound != 0 and num != 0 and highbound == 0:
			highbound = num
		elif lowbound != 0 and num == 0 and highbound != 0:
			highbound = highbound * 10 + num
	
	return lowbound,highbound

# Deal with the description of price attribute
def DealWithDetail(Original):
	Original = ''.join(Original).encode('utf-8')
	Original = Original.split("约")
	return Original[0]


"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
for target in range(701,801,100):
    readCSV = 'TotalURL_' + str(target) + '-' + str(target + 99) + '.csv'
  

    total = [('疾病', '疾病简介')]
    
    # 对readCSV 文件操作，读取疾病知识这一列的所有url

    data = pandas.read_csv(readCSV, encoding='GB18030')
    titleList = data[u'疾病']

    jbzsList = data[u'疾病简介']

    # write titles at the begining of the page
    writeCSV = u'疾病简介From_' + str(target) + '_to_' + str(target + 99 ) + '.csv'

    for temp in range(720,len(titleList)):
    	print temp
    	info = []

    	#获取疾病名称
    	title = titleList[temp]
        title = ''.join(title).encode('utf-8')

        #获取URL
        url = jbzsList[temp]
        #url中存在nan，只保留正确的url，这些url都是以http开头，所以通过正则匹配来解决
        m = re.match('^http', str(url))
        if m:
            print url
            print '-------------------------------------------------------'

            time.sleep(0.5)
            source = getPage(url,'GB18030')
            if source == None:
                continue
            price = source.xpath('//div[@class="chi-know"]/dl[3]/dd[2]/text()')
           
            if price:
              	lowbound,highbound = DealWithPrice(price)
              	detail = DealWithDetail(price)
              	item = [(title,detail,lowbound,highbound)]
              	WriteToCSV(writeCSV,item,temp)
            else:
             	print "No information"

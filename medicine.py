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
def WriteToCSV(csvName, text,temp):
    if temp == 0:
        title = [("通用名称","商品名称","英文名称","成分","功能主治","用法用量","不良反应","禁忌","注意事项","特殊人群用药","药理相互作用","药理作用","贮藏","有效期","批准文号","企业名称","生产地址","联系电话","对应疾病")]
        title = pandas.DataFrame(title)
        title.to_csv(csvName,encoding='GB18030', header=False, index=False,mode='a')
    paper = pandas.DataFrame(text)
    paper.to_csv(csvName, encoding='GB18030', header=False, index=False, mode='a')

# 处理药品名字
def DealWithTitle(source):
    items = source.xpath('//div[@class="tab_box"]/div/dl/dt/text()')
    result = []
    for item in items:
        item = ''.join(item)
        item = item.encode('utf-8')
        result.append(item)
    return result

# 处理药品每一项的URL
def Url_query(source,index):
    index = index + 1
    item_url = '//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/p/text()|//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/text()|//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/a/text()'
    items = source.xpath(item_url)
    items = ''.join(items)
    items = items.encode('utf-8')
    items = items.replace('\t','').replace('\n','').replace('\r','').replace(' ','').replace('  ','')
    return items

def DealwithNames(source,index):
    index = index + 1
    item_url = '//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/p/text()|//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/text()|//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/a/text()'
    items = source.xpath(item_url)
    result = []
    
    #处理特殊字符
    for item in items:
        item = item.replace('\n','').replace('\r','').replace(' ','')
        item = item.encode('utf-8')
        result.append(item)
    
    #对名称中不同的字段进行处理
    spmc = ""
    tymc = ""
    ywmc = ""

    for names in result:
        tags = names.split("：")
        if tags[0] == "商品名称":
            spmc = tags[1]
        elif tags[0] == "通用名称":
            tymc = tags[1]
        elif tags[0] == "英文名称":
            ywmc = tags[1]
    ywmc = DealWithEnglishNames(ywmc)
    return spmc,tymc,ywmc

#处理英文字段空格被取消的问题
def DealWithEnglishNames(Original):
    result = ''
    for letter in Original:
        if letter >= 'a' and letter <= 'z':
            result = result + letter
        elif letter >= 'A' and letter <= 'Z':
            result = result + " " + letter
    if len(result) < 5:
        return Original
    return result

#处理生产厂家
def DealWithCompany(source,index):

    index = index + 1
    item_url = '//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/p/text()|//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/text()|//div[@class="tab_box"]/div/dl[' + str(index) + ']/dd/a/text()'
    items = source.xpath(item_url)
    result = []

    #处理特殊字符
    for item in items:
        item = item.replace('\n','').replace('\r','').replace(' ','')
        item = item.encode('utf-8')
        result.append(item)

    #对生产厂家中不同的字段进行处理
    company = ""
    number = ""
    address = ""

    for things in result:
        tags = things.split("：")
        if tags[0] == "企业名称":
            company = tags[1]
        elif tags[0] == "生产地址":
            address = tags[1]
        elif tags[0] == "联系电话":
            number = tags[1]
    return company,address,number




"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
"""-----main------------------------------------------------"""
for target in range(1,801,100):
    readCSV = 'TotalURL_' + str(target) + '-' + str(target + 99) + '.csv'
  

    total = [('疾病', '药品及生产厂商')]
    
    # 对readCSV 文件操作，读取常用药品这一列的所有url

    data = pandas.read_csv(readCSV, encoding='GB18030')
    titleList = data[u'疾病']

    cyypList = data[u'常用药品']
    # write titles at the begining of the page
    writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '.csv'

    for temp in range(0,len(titleList)):
        print temp
        # if temp < 101:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_1.csv'
        # elif temp < 201:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_2.csv'
        # elif temp < 301:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_3.csv'
        # elif temp < 401:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_4.csv'
        # elif temp < 501:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_5.csv'
        # elif temp < 601:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_6.csv'
        # elif temp < 701:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_7.csv'
        # elif temp < 801:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_8.csv'
        # elif temp < 901:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_9.csv'
        # else:
        #     writeCSV = u'常用药品From_' + str(target) + '_to_' + str(target + 99 ) + '_10.csv'

        info = []

        # 疾病名称
        title = titleList[temp]
        title = ''.join(title).encode('utf-8')
        # print str(temp) + ':'+title
   

        # 获取url
        url = cyypList[temp]
        # url中存在nan，只保留正确的url，这些url都是以http开头，所以通过正则匹配来解决
        m = re.match('^http', str(url))
        if m:
            print url
            print '-------------------------------------------------------'

            source = getPage(url,'GB18030')
            if source == None:
                continue
            drugName = source.xpath('//div[@class="chi-drug"]/ul/li/h4/a/text()')
            manufacturer = source.xpath('//div[@class="chi-drug"]/ul/li/p/i/text()')
            drug_url = source.xpath('//div[@class="chi-drug"]/ul/li/h4/a/@href')
            information = []
            for every_drug in drug_url:
                component = ''
                indication = ''
                usage = ''
                reaction = ''
                avoid = ''
                attention = ''
                special_person = ''
                mut_effect = ''
                effect = ''
                storage = ''
                period = ''
                names = ''
                number = ''
                indication = ''
                company = ''
                info_url = str(every_drug) + '/manual'
                source_ = getPage(info_url, 'GB18030')
                if source_ == None:
                    continue
                title_ = DealWithTitle(source_)
                for index in range(len(title_)):
                    word = title_[index]
                    if word == '【成份】' or word == '【主要原料】':
                        component = Url_query(source_,index)
                    elif word == '【药品名称】' or word == '【产品名称】':
                        spmc,tymc,ywmc = DealwithNames(source_,index)
                    elif word == '【用法用量】':
                        usage = Url_query(source_,index)
                    elif word == '【不良反应】':
                        reaction = Url_query(source_,index)
                    elif word == '【禁忌】' or word == '【不适宜人群】':
                        avoid = Url_query(source_,index)
                    elif word == '【注意事项】':
                        attention = Url_query(source_,index)
                    elif word == '【特殊人群用药】' or word == '【适宜人群】':
                        special_person = Url_query(source_,index)
                    elif word == '【药物相互作用】':
                        mut_effect = Url_query(source_,index)
                    elif word == '【药理作用】':
                        effect = Url_query(source_,index)
                    elif word == '【贮藏】':
                        storage = Url_query(source_,index)
                    elif word == '【有效期】' or word == '【保质期】':
                        period = Url_query(source_,index)
                        period = period.replace('。','')
                    elif word == '【批准文号】':
                        number = Url_query(source_,index)
                    elif word == '【生产企业】' or word == '【生产厂家】':
                        company,address,phoneNumber = DealWithCompany(source_,index)
                        company = DealWithEnglishNames(company)
                        address = DealWithEnglishNames(address)
                    elif word == '【说明书修订日期】':
                        pass
                    else:
                        indication = Url_query(source_,index)
                sublist = (tymc,spmc,ywmc,component,indication,usage,reaction,avoid,attention,special_person,mut_effect,effect,storage,period,number,company,address,phoneNumber,title)
                information.append(sublist)
            WriteToCSV(writeCSV, information,temp)

        else:
            #无信息需要特殊处理
            print '无信息'
            print '-------------------------------------------------------'
           



# -*- coding: utf-8 -*-
import urllib2
import lxml.html as HTML
import pandas
import requests
import csv
import string

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

def getInfo(title,Singleurl):
	htmlSource = getPage(Singleurl,'GB18030')
	overview = htmlSource.xpath('//dd[@id="intro"]/p/text()')
	overview = ''.join(overview)
	

	total_reason = []
	total_possible_dis = []
	total_details = []
	total_drugs = []
	total_checks = []
	total_symptom = []
	total_names = []
	total_overview = [overview]
	
	#sub pages of main page
	url_reason = Singleurl + "zzqy/"
	urL_content = Singleurl + "zdxs/"
	url_types = Singleurl + "jcjb/"
	url_ = [url_reason,urL_content,url_types]


	#get the information of subpage of current disease
	for i in range(len(url_)):
		request_ = urllib2.Request(url_[i], headers=headers)
		response_ = urllib2.urlopen(request_)
		content_ = response_.read()
		content_ = content_.decode('GB18030')
		htmlSource_ = HTML.fromstring(content_)

    	#causes and possible diseases 
		if i == 0:
			reason = htmlSource_.xpath('//div[@class = "item catalogItem"]/p/a/text()|//div[@class = "item catalogItem"]/p/text()|//div[@class = "item catalogItem"]/p/span/text()')
			reason = ''.join(reason)
			total_reason.append(reason)
			possible_dis = htmlSource_.xpath('//tr/td[@class="name"]/a/text()')
			possible_dis =' '.join(possible_dis)
			total_possible_dis.append(possible_dis)
		

		# print reason.encode('utf-8'),possible_dis.encode('utf-8')

		elif i == 1:
			details = htmlSource_.xpath('//div[@class = "item catalogItem"]/p/text()|//div[@class = "item catalogItem"]/p/a/text()')
			details = ''.join(details)
			total_details.append(details)
			# print details.encode('utf-8')
			drugs = htmlSource_.xpath('//div[@id="relateDrug"]/dl/dd/h4/a/text()')
			drugs = ','.join(drugs)
			total_drugs.append(drugs)
			# print drugs.encode('utf-8')
		
	
		else:
			checks = htmlSource_.xpath('//div[@class="checkbox-data"]/table/tbody/tr/td/a/text()')

			checks = checks[::2]
			checks = ','.join(checks)
			total_checks.append(checks)
			# print checks.encode('utf-8')
			symptom = htmlSource_.xpath('//div[@class="item"]/ul/li/dl/dt/a/text()')
			symptom = ','.join(symptom)
			total_symptom.append(symptom)
			#print symptom.encode('utf-8')
	items = [(title,Singleurl,overview,reason,possible_dis,details,drugs,checks,symptom)]
	return items



def getPage(url, encoding):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    source = HTML.fromstring(response.read().decode(encoding))
    return source







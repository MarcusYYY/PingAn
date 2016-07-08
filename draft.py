set up user agent


url = 'http://jbk.39.net/zhengzhuang/ks/'

htmlSource = getPage(url,'GB18030')


total_reason = ["症状起因"]
total_possible_dis = ["可能疾病"]
total_details = ["诊断详述"]
total_drugs = ["对症药品"]
total_checks = ["常见检查"]
total_symptom = ["相似症状"]
total_names = ["疾病名称"]
total_overview = ["疾病综述"]

name = htmlSource.xpath('//div[@class="tik clearfix"]/a/h1/text()')
name = ''.join(name)
total_names.append(name)
overview = htmlSource.xpath('//dd[@id="intro"]/p/text()')
overview = ''.join(overview)
total_overview.append(overview)
# classification = htmlSource.xpath('//div[@class = "item type"]/ul/li/a/text()')
# classification = classification[:len(classification)-1]
# classification = ','.join(classification)

reason = []
possible_dis = []
details = []
drugs = []
checks = []
symptom = []
items = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

#sub pages of main page
url_reason = url + "zzqy/"
urL_content = url + "zdxs/"
url_types = url + "jcjb/"
url_ = [url_reason,urL_content,url_types]


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
		total_details.append(reason)
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

# if classification:
# 	items = [name,overview,classification,reason,possible_dis,details,drugs,checks,symptom]
# else:
# items = [name,overview,reason,possible_dis,details,drugs,checks,symptom]


items = [total_names,total_overview,total_reason,total_possible_dis,total_details,total_drugs,total_checks,total_symptom]
 
#matrix transpose
items = map(list,zip(*items))



#output csv files
paper = pandas.DataFrame(items)
paper.to_csv("39.csv",encoding = 'utf-8',header = False,index = False,mode = 'a')

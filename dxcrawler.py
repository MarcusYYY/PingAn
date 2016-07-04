
import urllib2
import lxml.html as HTML
import pandas
import requests

#url of websites needed to got
file_url_num = [226,224,153,218,210]

# set up user agent
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
headers = {'User-Agent': user_agent}

item_ = []
totalTag = []
totalAuthor = []
totalContent = []
totalTime = []
totalTopic = []

for url in file_url_num:
	url_ = 'http://dxy.com/column/special/' + str(url) + '/'
	request = urllib2.Request(url_, headers=headers)
	response = urllib2.urlopen(request)

	#Analyze
	content = response.read()
	content = content.decode('utf-8')
	htmlSource = HTML.fromstring(content)

	itemurl = htmlSource.xpath('//div[@class="col-article-list col-article-list-search col-search"]/ul/li/dl/dt/a/@href')


	# compensate incompleted url
	for i in range(len(itemurl)):
		itemurl[i] = 'http://dxy.com' + itemurl[i] + '/'

	#get attributes of each page
	for singleUrl in itemurl:
		request = urllib2.Request(singleUrl, headers=headers)
		response = urllib2.urlopen(request)
		content = response.read()
		content = content.decode('utf-8')
		htmlSource = HTML.fromstring(content)
		#get the author
		singleAuthor = htmlSource.xpath('//p[@class="info"]/span[@class = "author"]/a/text()')
		totalAuthor.append(singleAuthor)
		#get tags
		singleTag =  htmlSource.xpath('//div[@class="mod-tag mt50 J-col-tag"]/a/text()')
		totalTag.append(singleTag)
		#get time
		singleTime = htmlSource.xpath('//p[@class="info"]/span[@class = "time"]/text()')
		totalTime.append(singleTime)
		#get topics
		singleTopic = htmlSource.xpath('//div[@class="pg-article-hd"]/h1/text()')
		totalTopic.append(singleTopic)
		#get contents
		singleContent = htmlSource.xpath('//div[@class="editor-body"]/p/text()|//div[@class="editor-body"]/div/text()|//div[@class="editor-body"]/p/font/font/text()')
		totalContent.append(singleContent)

#matrix transpose
item_ = [totalTopic,totalTime,totalAuthor,totalTag,totalContent]
item_ = map(list,zip(*item_))
	
#output csv files

paper = pandas.DataFrame(item_)
paper.to_csv("dxy.csv",encoding = 'GB18030',header = False,index = False,mode = 'a')





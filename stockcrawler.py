# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:56:43 2016

@author: MarcusYYY
"""

from bs4 import BeautifulSoup
#import re
import os
import urllib2
import ssl
import csv
import tushare as ts

'''------获得股票代码-----------------------------------------------------------------------'''
def FindStockCode():
    aa=ts.get_stock_basics();
    return aa.index
    



'''-----输出每只股票的信息至test.csv---------------------------------------------------------'''

def CodeToCsv(CurCode,csvWriter):    
    '''-----伪装成Chrome进行访问-----------------------------------------------------------------'''
    #User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36
    #Cookie: U_TRS1=00000007.5076973.54a7dec0.f7881341; U_TRS2=00000007.5166973.54a7dec0.c05f966b; SINAGLOBAL=111.186.4.149_1420287681.32005; Apache=111.186.4.149_1420287681.222819; vjuids=8544a24e2.14aafbe29b1.0.fdd0961d; SGUID=1420287683349_45852867; SessionID=s94fpi0s0nqldkksgo097ih5t0; UOR=www.google.com.hk,news.sina.com.cn,; ULV=1453634833275:1:1:1:111.186.4.149_1420287681.222819:; sso_info=v02m6alo5qztYGbpp2lk4aVoZqClYWNkpWBkZKUuI6SlYWNspS5jIKVgZCSlYWNgpWCjoKVgpGClYWNkpWBjoKUuI2SmbWalpC9jZOguIyTmLWMg4S1jIDAwA==; WEB2_APACHE2_GD=08b1373f0ed9ce5f3c4eb9136663d53a; VARNISH-gd=765e270810a4dcfa0395acc24766b691; SINA_FINANCE=AngeLeah%E5%AE%89%E7%90%AA%E4%B8%BD%E5%A8%85%3A5881650150%3A4; SR_SEL=1_511; usrmd=usrmdinst_31; SUS=SID-5881650150-1462189783-XD-ujwqb-31dfdbe56f9f1a485ab433d258fbe5b9; SUB=_2A256I06HDeTxGeNG41MX9S7NzjyIHXVZWSdPrDV_PUNbvtAPLWrbkW9LHetyzBnV9lpI50OcDM0bSjYBw4tlyg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWYHCAQwhQErr8Bru6pQgdc; ALF=1493725783; FINA_V_S_2=sh600030,sz300411,sz002478,sh600089,sh000001; FIN_ALL_VISITED=sh600001%2Csh600030%2Csz300411%2Csz002478%2Csh600089%2Csh000001; SUE=es%3De5fe6f02dfd9a841c06db72e80432019%26ev%3Dv1%26es2%3Df6f2b5ad09180461c1fcb56667e361ac%26rs0%3DBOZOLbnrSQBOYXBPjjx9kq%252BJ%252FpzNssGJcEcZNmdU7g7acOoeh0CxsuDRrmsAKIguOq0tghrJekmNQEDhjlqB6AB6P8NWV3okYK3ns7SrdG06G7lYDQUobecFlSGXmg3I7%252FZ1RaaRqxCN9pHdPozAapfsGtkzgipTkGMmCBcyXSc%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1462189783%26et%3D1462356405%26d%3D40c3%26i%3De5b9%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26lt%3D7%26uid%3D5881650150%26user%3Dl_studios%2540163.com%26ag%3D4%26name%3Dl_studios%2540163.com%26nick%3DAngeLeah%25E5%25AE%2589%25E7%2590%25AA%25E4%25B8%25BD%25E5%25A8%2585%26sex%3D1%26ps%3D0%26email%3D%26dob%3D%26ln%3D%26os%3D%26fmp%3D%26lcp%3D; vjlast=1462272655.1462272655.10

    request = urllib2.Request('http://vip.stock.finance.sina.com.cn/corp/go.php/vGP_RelatedTrade/stockid/'+str(CurCode)+'.phtml')  
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')  
    response = urllib2.urlopen(request)  
    soup=BeautifulSoup(response.read())
    
    
    
    '''文件所在区域'''
    x = soup.body.find('div',id="wrap")\
                    .find('div',id="main")\
                    .find('div',id="center")\
                    .find('div',{'class': 'centerImgBlk'})\
                    .find('div',id="con02-1");
    if x.find('table',id='collectFund_1'):
        xx=x.find('table',id='collectFund_1')\
                    .find('tbody');
                    
        '''公告时间(仅保留日期)'''
        #for i in xx.findAll('thead'):
        #    print i.find('a').attrs['name'][:10]
        #    
        '''------从html中获取对应的文件------------------------------------------'''
        xtime=xx.findAll('thead') #'''公告时间'''
        num  = len(xtime)         #'''公告次数'''
        JiaCo  = xx.findAll('strong',text="甲公司")
        YiCo   = xx.findAll('strong',text="乙公司")
        DingJia= xx.findAll('strong',text="定价依据")
        JianJie= xx.findAll('strong',text="交易简介")
        LeiBie= xx.findAll('strong',text="交易类别")
        JinE= xx.findAll('strong',text="交易金额")
        HuoBi= xx.findAll('strong',text="货币代码")
        
        #for i in range(num):
        #    print "交易时间=",xtime[i].find('a').attrs['name'][:10]
        #    print "甲公司=",JiaCo[i].parent.next_sibling.text
        #    print "乙公司=",YiCo[i].parent.next_sibling.text
        #    print "定价依据=",DingJia[i].parent.next_sibling.text
        #    print "交易简介=",JianJie[i].parent.next_sibling.text
        #    print "交易类别=",LeiBie[i].parent.next_sibling.text
        #    print "交易金额=",JinE[i].parent.next_sibling.text
        #    print "货币代码=",HuoBi[i].parent.next_sibling.text,'\n'
        #
        '''-------写入csv文档中--------------------------------------------------''' 
        for i in range(num):
            csvWriter.writerow([CurCode.encode('gb2312','ignore'),\
                                xtime[i].find('a').attrs['name'][:10],\
                                JiaCo[i].parent.next_sibling.text.encode('gb2312','ignore'),\
                                YiCo[i].parent.next_sibling.text.encode('gb2312','ignore'),\
                                DingJia[i].parent.next_sibling.text.encode('gb2312','ignore')+JianJie[i].parent.next_sibling.text.encode('gb2312','ignore'),\
                                LeiBie[i].parent.next_sibling.text.encode('gb2312','ignore'),\
                                JinE[i].parent.next_sibling.text.encode('gb2312','ignore'),\
                                HuoBi[i].parent.next_sibling.text.encode('gb2312','ignore')
                                ]);
                            
        return num

if __name__=="__main__":
    '''---- 全局取消证书验证（去除打开网页时SSL限制）-------------------------------------------'''
    ssl._create_default_https_context = ssl._create_unverified_context
    x = []
    
    '''------打开csv并执行编写----------------------------------------------------------------------------'''
    outputFp=open('./test.csv', 'ab');
    csvWriter = csv.writer(outputFp, dialect='excel');
    StockCode=FindStockCode()
    TotalNum=len(StockCode);
    for i in range(TotalNum):
        num = CodeToCsv(StockCode[i],csvWriter) or 0;
        print "股票", StockCode[i],"的",str(num),'条关联交易已记录，还剩',str(TotalNum-i-1),"个股票"
    outputFp.close();



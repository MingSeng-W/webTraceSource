# coding:utf-8
import re
import bs4
import os
import mysql.connector
import mysql
import urllib
import urllib2
import time
import bs4
import cookielib
class weiboCrawlser:
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support)
    urllib2.install_opener(opener)
    index=1
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'Cookie':'SINAGLOBAL=2580452964109.3633.1468546273913; _s_tentry=www.doc88.com; TC-Page-G0=9183dd4bc08eff0c7e422b0d2f4eeaec; Apache=5174620901646.758.1472833693191; ULV=1472833693197:5:1:1:5174620901646.758.1472833693191:1471356725919; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; TC-V5-G0=1e4d14527a0d458a29b1435fb7d41cc3; login_sid_t=33ce6566732e1ba914cfaa364629f553; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; YF-V5-G0=a5a264208a5b5a42590274f52e6c7304; YF-Page-G0=416186e6974c7d5349e42861f3303251; SSOLoginState=1472992590; ULOGIN_IMG=14735648788003; UOR=www.micmiu.com,widget.weibo.com,blog.sina.com.cn; WBStorage=86fb700cbf513258|undefined; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625IMXIZaZNdIOze7TpK7pgyrlRjBWm_-WE0nezWQA1bT4.; SUB=_2A2560a5nDeTxGeNP7FcQ8yvJyj-IHXVZppivrDV8PUNbmtAKLXXDkW9PIF7E40Dhn5WbcQMzblF-aUYH-g..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFnL1Xf6TWVe-5ZwiAl2ySh5JpX5K2hUgL.Fo-pS0-pe0-feKe2dJLoI08kPEH8SFHFxFHWeFH8SC-ReFHFBEH8SCHFxC-4SEH8Sb-RBbHWSCH8Sb-4BE-R1Hvk; SUHB=0ebtQ7K75EDsPR; ALF=1505169846; un=15025019730; wvr=6'
    }

    def __init__(self,keyword):
        self.keyword=keyword
        self.itemIndex=0

    def connectMysql(self,username,link,weibotext,time,date,myindex):
        config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'port': '3306',
            'database': 'weibostore'
        }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        add_user = (
        "INSERT INTO user(username,link,weibotext,time,date,myindex) VALUES(%(username)s,%(link)s,%(weibotext)s,%(time)s,%(date)s,%(myindex)s)")
        data_user = {
            'username': username,
            'weibotext': weibotext,
            'time': time,
            'date':date,
            'link': link,
            'myindex':str(self.index)
        }
        self.index=self.index+1
        cursor.execute(add_user, data_user)
        conn.commit()
        cursor.close()
        conn.close()

    def getBS4Obj(self,filename):
        with open(filename, 'r') as f:
            temp = f.read()
            html =bs4.BeautifulSoup(temp,'lxml',from_encoding="utf-8")
        return  html

    def getpage(self,flag,page,filename):
        if flag==0:
            url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&Refer=g'
        else:
            url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&page='+str(page)
        req = urllib2.Request(url=url, headers=self.header)
        res = urllib2.urlopen(req)
        html = res.read()
        self.parseUnicode(filename=filename,html=html)


    def parseUnicode(self,filename,html):
        with open(filename, 'w') as f:
            view = re.findall('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>', html)
            for i in view:
                r = i.encode('utf-8').decode('unicode_escape').encode('utf-8')
                s = r.replace("\/", "/")
                f.write(s)

    def getPageWithTime(self,page,time,filename):
        url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&page=' + str(page) + '&timescope=custom::' + time
        req = urllib2.Request(url=url, headers=self.header)
        res = urllib2.urlopen(req)
        html = res.read()
        self.parseUnicode(filename=filename, html=html)

    def getfirstpage(self):
        self.getpage(0,0,'fisrtpage.html')

    def getTotalPageNum(self):
            self.getfirstpage()
            html = self.getBS4Obj('fisrtpage.html')
            totalpage=1
            try:
                    divcon=html.find(attrs={'class':'layer_menu_list W_scroll'})
                    licon=divcon.find('ul').find_all('li')
                    totalpage=len(licon)
            except:
                    pass
            return  totalpage
    def parseTotalPageHtml(self,filename):
        totalPage=1
        html = self.getBS4Obj(filename)
        try:
            divcon = html.find(attrs={'class': 'layer_menu_list W_scroll'})
            licon = divcon.find('ul').find_all('li')
            totalPage = len(licon)
        except:
             totalPage=0
        return totalPage

    def getWeiboAry(self,filename):
        html = self.getBS4Obj(filename=filename)
        weiboconAry = html.find_all(attrs={'class': 'WB_cardwrap S_bg2 clearfix'})
        return weiboconAry

    def getPersonInfo(self,weiboCon):
        text = weiboCon.find('p', attrs={'class': 'comment_txt'}).text
        temp = weiboCon.find(attrs={'class': 'face'}).find('a')
        name = temp['title']
        link = temp['href']
        timeTemp = weiboCon.find(attrs={'class': 'feed_from W_textb'}).find('a')
        time = timeTemp['title']
        date = timeTemp['date']
        return name,text,time,date,link

    def getWeiBoTime(self,weibo):
        timeTemp = weibo.find(attrs={'class': 'feed_from W_textb'}).find('a')
        time = timeTemp['title']
        return time

    def getPerson(self):
            totalpage=str(self.getTotalPageNum())
            totalpageTemp=int(totalpage)+1
            for i in range(1,totalpageTemp):
                self.getpage(1,str(i),'fisrtpage.html')
                weiboAry=self.getWeiboAry('fisrtpage.html')
                length=len(weiboAry)
                self.getEveryOne(weiboAry=weiboAry)
                print "downloading page ",i
                time.sleep(10)

    def getStartTimeTemp(self):
        startTime=''

        return startTime

    def handleTime(self,startTime):
        temp=time.strptime(startTime,"%Y-%m-%d %H:%M")
        y,m,d,h=temp[0:4]
        return str(y)+'-'+str(m)+"-"+str(d)+"-"+str(h)

    def getStartTime(self):
        startTime=''
        totalPage=self.getTotalPageNum()
        flag=1
        self.getpage(1,totalPage,"firstPage.html")
        weiboAry=self.getWeiboAry("firstPage.html")
        lastIndex=len(weiboAry)-1
        startTime=self.getWeiBoTime(weiboAry[lastIndex])
        if totalPage==50:
            while flag==1:
                self.getPageWithTime(1,self.handleTime(startTime),"middleTime.html")
                totalPage=self.parseTotalPageHtml("middleTime.html")
                self.getPageWithTime(page=totalPage,time=self.handleTime(startTime),filename="middleTime.html")
                weiboAry=self.getWeiboAry("middleTime.html")
                lastIndex=len(weiboAry)-1
                weiboTemp=weiboAry[lastIndex]
                startTime=self.getWeiBoTime(weiboTemp)
                if totalPage!=50:
                    flag=0
        return startTime


    def getEveryOne(self,weiboAry):
        for weibo in weiboAry:
            name, text, time, date, link = self.getPersonInfo(weibo)
            self.connectMysql(myindex=self.itemIndex,username=name, link=link, time=time, date=date, weibotext=text)
            self.itemIndex=self.itemIndex+1



wb = weiboCrawlser(keyword='10-100元梁静茹演唱会')
print wb.getStartTime()



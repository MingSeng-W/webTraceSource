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
    'Cookie':'SINAGLOBAL=2580452964109.3633.1468546273913; _s_tentry=www.doc88.com; TC-Page-G0=9183dd4bc08eff0c7e422b0d2f4eeaec; Apache=5174620901646.758.1472833693191; ULV=1472833693197:5:1:1:5174620901646.758.1472833693191:1471356725919; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; TC-V5-G0=1e4d14527a0d458a29b1435fb7d41cc3; login_sid_t=33ce6566732e1ba914cfaa364629f553; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; YF-V5-G0=a5a264208a5b5a42590274f52e6c7304; YF-Page-G0=416186e6974c7d5349e42861f3303251; un=15025019730; wvr=6; SSOLoginState=1472992590; ULOGIN_IMG=14730046003746; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625DzwgGKrfvY-WZWP3lxj3Lk81VVVw0AI1ukCUFCyTMns.; SUB=_2A25614srDeTxGeNL7FUZ-CfJzT2IHXVZpPvjrDV8PUJbmtBeLVLlkW88fu29zcQ1vlUqO_0XK3Dw8wkIHg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MINdBKrimGBVg4AxBhZ3J5JpX5o2p5NHD95QfSKMN1hn4SKqpWs4Dqcjpi--fi-2Ei-2Ri--4iK.fiKLhi--fiK.fi-2ci--fiK.fi-2ci--fiK.fi-2cTK57e7tt; SUHB=0tKaieLlJkxMtT; ALF=1505043816; UOR=www.micmiu.com,widget.weibo.com,www.baidu.com'
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

        elif flag==8:
            url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&page=' + page+'&timescope=custom::'+time
        else:
            url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&page='+page
        req = urllib2.Request(url=url, headers=self.header)
        res = urllib2.urlopen(req)
        with open(filename, 'w') as f:
            html = res.read()
            view = re.findall('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>', html)
            for i in view:
                r = i.encode('utf-8').decode('unicode_escape').encode('utf-8')
                s = r.replace("\/", "/")
                f.write(s)

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


    def getPerson(self):
            totalpage=str(self.getTotalPageNum())
            self.getpage(1,totalpage,'fisrtpage.html')
            weiboAry=self.getWeiboAry('fisrtpage.html')
            length=len(weiboAry)
            self.getEveryOne(weiboAry=weiboAry)

    def getEveryOne(self,weiboAry):
        for weibo in weiboAry:
            name, text, time, date, link = self.getPersonInfo(weibo)
            self.connectMysql(myindex=self.itemIndex,username=name, link=link, time=time, date=date, weibotext=text)
            self.itemIndex=self.itemIndex+1
            print


wb = weiboCrawlser(keyword='zv事件')
wb.getFirstPerson()
# for i in range(1, 7):
#     wb.test(i,keyword)
#     time.sleep(20)
# print 'finish all'


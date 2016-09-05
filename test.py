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
        'Cookie':'SINAGLOBAL=2580452964109.3633.1468546273913; _s_tentry=www.doc88.com; TC-Page-G0=9183dd4bc08eff0c7e422b0d2f4eeaec; Apache=5174620901646.758.1472833693191; ULV=1472833693197:5:1:1:5174620901646.758.1472833693191:1471356725919; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; TC-V5-G0=1e4d14527a0d458a29b1435fb7d41cc3; login_sid_t=33ce6566732e1ba914cfaa364629f553; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; YF-V5-G0=a5a264208a5b5a42590274f52e6c7304; YF-Page-G0=416186e6974c7d5349e42861f3303251; un=15025019730; UOR=www.micmiu.com,widget.weibo.com,login.sina.com.cn; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625vWzLW1imdDWEXEN7EseMy549ayrBfg5NnhACn2gwT3E.; SUB=_2A256z4lGDeTxGeNL7FUZ-CfJzT2IHXVZvP2OrDV8PUNbmtBeLXWikW9Y-RlzQQMLo1M4csiverelxsWFsA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MINdBKrimGBVg4AxBhZ3J5JpX5KzhUgL.Fo-fS0MR1h.fSo22dJLoI02LxK-LBKzLBKnLxK.L1K-L1-eLxK-L1K-LBKqLxK-L1K-LBKqLxK-L1K-LBKq_eh50; SUHB=0ftZjw-62RxhjA; ALF=1504521366; SSOLoginState=1472985366; wvr=6'
    }

    def __init__(self,keyword):
        self.keyword=keyword


    def connectMysql(self,username,link,weibotext,time,date):
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
            'link': link,
            'username': username,
            'weibotext': weibotext,
            'time': time,
            'date':date,
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
            url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1'
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



    # 获得微博页面的数组函数
    def getweiboPageAry(self,page,filename):
        self.getpage(1,page,filename)
        html=self.getBS4Obj(filename=filename)
        weiboAry=html.find_all(attrs={'class':'WB_cardwrap S_bg2 clearfix'})
        return weiboAry

    def getWeiboInfo(self,weiboCon):
        text = weiboCon.find('p', attrs={'class': 'comment_txt'}).get_text()
        temp = weiboCon.find(attrs={'class': 'face'}).find('a')
        name = temp['title']
        link = temp['href']
        timeTemp = weiboCon.find(attrs={'class': 'feed_from W_textb'}).find('a')
        mytime = timeTemp['title']
        date = timeTemp['date']
        self.connectMysql(username=name, link=link, time=mytime, date=date, weibotext=text)

    def getFirstTime(self, totalpage,filename):
        temptime=''
        tmepUnix=''
        weiboAry=self.getweiboPageAry(totalpage,filename)
        length=len(weiboAry)-1
        weibocon=weiboAry[length]
        temptime=weibocon['title']
        tmepUnix=weibocon['date']
        return temptime,tmepUnix
    def judgePage(self,totalpage):


    def getPerson(self):
            totalpage=str(self.getTotalPageNum())
            totalpagetemp=int(totalpage)
            print "totalpage",totalpage
            if totalpage
            for i in range(1,totalpagetemp+1):
                self.getpage(1,str(i),'originalpage.html')
                html=self.getBS4Obj('originalpage.html')
                weiboconAry=html.find_all(attrs={'class':'WB_cardwrap S_bg2 clearfix'})
                length=len(weiboconAry)
                for k in range(0,length):
                        weiboCon=weiboconAry[k]
                        self.getWeiboInfo(weiboCon)
                print "finish page",i
                time.sleep(10)







# def connectMysql(username,userid,weibotext,weiboid):
#     config={
#         'user':'root',
#         'password':'',
#         'host':'localhost',
#         'port':'3306',
#         'database':'weibostore'
#     }
#     conn=mysql.connector.connect(**config)
#     cursor=conn.cursor()
#     add_user=("INSERT INTO user(username,link,weibocontent) VALUES(%(userid)s,%(username)s,%(weiboid)s,%(weibocontent)s)")
#     data_user={
#         'userid':userid,
#         'username':username,
#         'weiboid':weiboid,
#         'weibocontent':weibotext
#     }
#
#     cursor.execute(add_user,data_user)
#
#     conn.commit()
#     result_set=cursor.fetchone()
#     print result_set
#     cursor.close()
#     conn.close()


keyword=raw_input("please in put the keyword:")
wb = weiboCrawlser(keyword=keyword)
wb.getPerson()
# for i in range(1, 7):
#     wb.test(i,keyword)
#     time.sleep(20)
# print 'finish all'


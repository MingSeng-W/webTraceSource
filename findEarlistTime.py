# coding:utf-8
import re
import bs4
import os
import urllib
import urllib2
import time
import bs4
import cookielib
from tool import timeCaclulate
import TextSimmliar
import dateItem


class weiboCrawlser:
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support)
    urllib2.install_opener(opener)
    headerIndex = 0

    def __init__(self, keyword,dataBaseName):
        self.keyword = keyword
        self.index = dateItem.getDataBaseIndex(dataBaseName)
        self.pageIndex=1
        self.startTime=""
        self.headerDict={
            "header0": {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Cookie': 'SINAGLOBAL=2580452964109.3633.1468546273913; TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; login_sid_t=a45730ec5784b903ccd5cf2b68f900b5; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; _s_tentry=-; Apache=7344403422873.24.1473897694479; ULV=1473897694486:6:2:1:7344403422873.24.1473897694479:1472833693197; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; wvr=6; SSOLoginState=1473932268; UOR=www.micmiu.com,widget.weibo.com,nav.uestc.edu.cn; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; WBStorage=86fb700cbf513258|undefined; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625Ux1KQTuM3GK_MLV983c5uhcPtv2OPLev6AmKqU3H9GM.; SUB=_2A2562WLlDeTxGeNL7FUZ-CfJzT2IHXVZr9MtrDV8PUNbmtBeLXP9kW-cQEsyWywHkvOO-rFK_UREfThubw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MINdBKrimGBVg4AxBhZ3J5JpX5K2hUgL.Fo-fS0MR1h.fSo22dJLoI02LxK-LBKzLBKnLxK.L1K-L1-eLxK-L1K-LBKqLxK-L1K-LBKqLxK-L1K-LBKq_eh50; SUHB=0BLYINmbub_KIo; ALF=1505642037; un=15520441791; YF-Page-G0=f70469e0b5607cacf38b47457e34254f'
        },
        "header1":{
            'Cookie': 'SINAGLOBAL=2580452964109.3633.1468546273913; TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; login_sid_t=a45730ec5784b903ccd5cf2b68f900b5; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; _s_tentry=-; Apache=7344403422873.24.1473897694479; ULV=1473897694486:6:2:1:7344403422873.24.1473897694479:1472833693197; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; wvr=6; UOR=www.micmiu.com,widget.weibo.com,nav.uestc.edu.cn; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; un=15520441791; YF-Page-G0=f70469e0b5607cacf38b47457e34254f; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625NA7-P8n5eYntovkd_zp9j9krVopWlPjflDbCvv4EtwU.; SUHB=0idbegACJ55I2V; SSOLoginState=1474107087; SUB=_2A2562WafDeTxGeNH71UQ9SfOzTyIHXVWIgrXrDV8PUJbkNBeLUn5kW18hvsWvX11ERSGl1Gb-kmxxzc6mw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5mrfxOUGAJ_1NSUcqGR8lz5JpX5oz75NHD95Qf1KBNeK-4eoq7Ws4DqcjAi--ciKn7iKL2i--RiK.4iK.pi--fi-isi-2Ni--ciKnXiKnpi--fi-z4i-zEi--Ri-20iKnEC-HHCBtt',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
        },
        "header2":{
            'Cookie': 'SINAGLOBAL=2580452964109.3633.1468546273913; TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; login_sid_t=a45730ec5784b903ccd5cf2b68f900b5; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; _s_tentry=-; Apache=7344403422873.24.1473897694479; ULV=1473897694486:6:2:1:7344403422873.24.1473897694479:1472833693197; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; wvr=6; UOR=www.micmiu.com,widget.weibo.com,nav.uestc.edu.cn; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; un=15520441791; YF-Page-G0=f70469e0b5607cacf38b47457e34254f; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625NA7-P8n5eYntovkd_zp9j9krVopWlPjflDbCvv4EtwU.; SUHB=0idbegACJ55I2V; SSOLoginState=1474107463; SUB=_2A2562WgWDeTxGeNH71oY-C_IyT-IHXVWIgherDV8PUJbkNBeLWLskW0nH_efcB8Y7D5YvYdc334ZkHqvqA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W50ERu6w4LLzU3RxeqVMdFu5JpX5oz75NHD95Qf1KBR1KnpShz0Ws4Dqcjci--NiK.4i-i2i--NiKLWiK.4i--4i-zEiKLhi--RiKyWi-zpi--Ri-2XiK.Ei--Ri-zXi-8h',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
        },
        "header3":{
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Cookie':'SINAGLOBAL=2580452964109.3633.1468546273913; TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; login_sid_t=a45730ec5784b903ccd5cf2b68f900b5; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; _s_tentry=-; Apache=7344403422873.24.1473897694479; ULV=1473897694486:6:2:1:7344403422873.24.1473897694479:1472833693197; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; YF-Page-G0=f70469e0b5607cacf38b47457e34254f; WBStorage=86fb700cbf513258|undefined; UOR=www.micmiu.com,widget.weibo.com,login.sina.com.cn; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625-fvZHyP-Kt-Hmx-XUeGkBRQfgayIdaLwjPZhZ_jln-A.; SUB=_2A2562TvzDeTxGeBO6lQW9i_NzjSIHXVZryo7rDV8PUNbmtBeLVXykW9ifnJDOsx_jDzRutFSzTIddLwGKw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFgn5kd-ClvdUSLrs2E8NiV5JpX5K2hUgL.Foq7eKqNSo2pSKn2dJLoIEBLxK-LBoeLBo5LxK-LBo.LB.zLxKnLB.-LBK.LxK-L1h.LBKMt; SUHB=01026h6IjXNJqb; ALF=1505656611; SSOLoginState=1474120611; un=13361049841; wvr=6; WBtopGlobal_register_version=058ac28f5e23153a'
        },
        "header4":{
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Cookie':'SINAGLOBAL=2580452964109.3633.1468546273913; TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; login_sid_t=a45730ec5784b903ccd5cf2b68f900b5; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; _s_tentry=-; Apache=7344403422873.24.1473897694479; ULV=1473897694486:6:2:1:7344403422873.24.1473897694479:1472833693197; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; YF-Page-G0=f70469e0b5607cacf38b47457e34254f; WBtopGlobal_register_version=058ac28f5e23153a; UOR=www.micmiu.com,widget.weibo.com,login.sina.com.cn; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625X0MEv6c9JWCXbIHWmmO1KX7rmfWIr2p29i-insQOkPY.; SUB=_2A2562SAzDeTxGeBO6lQW9i_IyjmIHXVZrxb7rDV8PUNbmtAKLWP7kW8T0dQvo7KBZC0OHcKj95to1moPVA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W54eRq2IsC1gCsCwP9LxQAy5JpX5K2hUgL.Foq7eKqNSo2XeK-2dJLoIEBLxK-L1hqL1KzLxK-LB.eL1heLxK-LBozL1h2LxK-L12BL1-2t; SUHB=0A0JqMm3F0VRAG; ALF=1505657826; SSOLoginState=1474121827; un=17086627806; wvr=6'
        },
        "header5":{
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Cookie':'SINAGLOBAL=2580452964109.3633.1468546273913; TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; login_sid_t=a45730ec5784b903ccd5cf2b68f900b5; TC-V5-G0=f88ad6a0154aa03e3d2a393c93b76575; _s_tentry=-; Apache=7344403422873.24.1473897694479; ULV=1473897694486:6:2:1:7344403422873.24.1473897694479:1472833693197; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; YF-Page-G0=f70469e0b5607cacf38b47457e34254f; WBtopGlobal_register_version=058ac28f5e23153a; WBStorage=86fb700cbf513258|undefined; UOR=www.micmiu.com,widget.weibo.com,login.sina.com.cn; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i6250tou2aTpU1ZxD3rYSzqfbC4zvkrLnKYd4qKclwWetCU.; SUB=_2A2562SFODeTxGeBO6lQW9irLyT-IHXVZrxWGrDV8PUNbmtAKLRjgkW9mXNrXvu6Vfix6-HVu7Ts3GUi6OQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ninPC8zl1p0UYpjvkBiyE5JpX5K2hUgL.Foq7eKqNSoBNeoe2dJLoIEBLxKnLBoBLBK2LxK-LBoML1-BLxKMLBK5L1h2LxKnL1heL1-et; SUHB=0d4Ory84_X6guK; ALF=1505658013; SSOLoginState=1474122014; un=18565476045; wvr=6'
        }
        }



    def getBS4Obj(self, filename):
        with open(filename, 'r') as f:
            temp = f.read()
            html = bs4.BeautifulSoup(temp, 'lxml', from_encoding="utf-8")
        return html

    def getpage(self, flag, page, filename):
        if flag == 0:
            url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&Refer=g'
        else:
            url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&page=' + str(page)
        temp = self.headerIndex % 6
        self.headerIndex+=1
        header = "header" + str(temp)
        req = urllib2.Request(url=url, headers=self.headerDict[header])
        res = urllib2.urlopen(req)
        html = res.read()
        self.parseUnicode(filename=filename, html=html)



    def parseUnicode(self, filename, html):
        with open(filename, 'w') as f:
            view = re.findall('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>', html)
            for i in view:
                r = i.encode('utf-8').decode('unicode_escape').encode('utf-8')
                s = r.replace("\/", "/")
                f.write(s)

    def getPageWithTime(self, page, time, filename):
        url = 'http://s.weibo.com/weibo/' + self.keyword + '&scope=ori&suball=1&page=' + str(
            page) + '&timescope=custom::' + time
        temp=self.headerIndex%6
        self.headerIndex+=1
        header="header"+str(temp)
        req = urllib2.Request(url=url, headers=self.headerDict[header])
        res = urllib2.urlopen(req)
        html = res.read()
        self.parseUnicode(filename=filename, html=html)

    def getfirstpage(self):
        self.getpage(0, 0, 'fisrtpage.html')

    def getTotalPageNum(self):
        self.getfirstpage()
        html = self.getBS4Obj('fisrtpage.html')
        totalpage = 1
        try:
            divcon = html.find(attrs={'class': 'layer_menu_list W_scroll'})
            licon = divcon.find('ul').find_all('li')
            totalpage = len(licon)
        except:
            pass
        return totalpage

    def parseTotalPageHtml(self, filename):
        totalPage = 1
        html = self.getBS4Obj(filename)
        try:
            divcon = html.find(attrs={'class': 'layer_menu_list W_scroll'})
            licon = divcon.find('ul').find_all('li')
            totalPage = len(licon)
        except:
            totalPage = 0
        return totalPage

    def getWeiboAry(self, filename):
        html = self.getBS4Obj(filename=filename)
        weiboconAry = html.find_all(attrs={'class': 'WB_cardwrap S_bg2 clearfix'})
        return weiboconAry

    def getPersonInfo(self, weiboCon):
        text = weiboCon.find('p', attrs={'class': 'comment_txt'}).text
        temp = weiboCon.find(attrs={'class': 'face'}).find('a')
        name = temp['title']
        link = temp['href']
        timeTemp = weiboCon.find(attrs={'class': 'feed_from W_textb'}).find('a')
        time = timeTemp['title']
        date = timeTemp['date']
        return name, text, time, date, link

    def getWeiBoTime(self, weibo):
        timeTemp = weibo.find(attrs={'class': 'feed_from W_textb'}).find('a')
        time = timeTemp['title']
        return time

    def getPerson(self,):
        totalpage = str(self.getTotalPageNum())
        totalpageTemp = int(totalpage) + 1

        for i in range(1, totalpageTemp):
            self.getpage(1, str(i), 'fisrtpage.html')
            weiboAry = self.getWeiboAry('fisrtpage.html')
            length = len(weiboAry)
            self.getEveryOne(weiboAry=weiboAry)
            print "downloading page ", self.pageIndex
            self.pageIndex += 1
            time.sleep(5)



    def getStartTimeTemp(self):
        startTime = ''

        return startTime

    def handleTime(self, startTime):
        temp = time.strptime(startTime, "%Y-%m-%d %H:%M")
        y, m, d, h = temp[0:4]
        return str(y) + '-' + str(m) + "-" + str(d) + "-" + str(h)

    def getStartTime(self):
        startTime = ''
        totalPage = self.getTotalPageNum()
        flag = 1
        self.getpage(1, totalPage, "firstPage.html")
        weiboAry = self.getWeiboAry("firstPage.html")
        lastIndex = len(weiboAry) - 1
        startTime = self.getWeiBoTime(weiboAry[lastIndex])
        if totalPage == 50:
            while flag == 1:
                self.getPageWithTime(1, self.handleTime(startTime), "middleTime.html")
                totalPage = self.parseTotalPageHtml("middleTime.html")
                self.getPageWithTime(page=totalPage, time=self.handleTime(startTime), filename="middleTime.html")
                weiboAry = self.getWeiboAry("middleTime.html")
                lastIndex = len(weiboAry) - 1
                weiboTemp = weiboAry[lastIndex]
                startTime = self.getWeiBoTime(weiboTemp)
                if totalPage != 50:
                    flag = 0
        self.startTime=startTime

    def getEveryOne(self, weiboAry):
        for weibo in weiboAry:
            name, text, time, date, link = self.getPersonInfo(weibo)
            dateItem.connectMysql(myindex=self.index, username=name, link=link, time=time, date=date, weibotext=text,similar='10.0',topic=self.keyword)
            self.index = self.index + 1


wb = weiboCrawlser(keyword='赵薇事件',dataBaseName="user")
wb.getPerson()







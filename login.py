#coding:utf-8
import sys
import re
import bs4
import os
import mysql.connector
import mysql
import urllib
import urllib2
from urllib2 import HTTPError, URLError
import hashlib
import base64
import rsa
import binascii
import time
import cookielib
import json
from dataStore import weiboLinkList
from dataStore import weiboNode


class weiboLogin:
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    'Cookie':'_T_WM=921d1ec11563b9afbf3ee4b2cf74d20b; WEIBOCN_FROM=page_1004062812335943_profile; ALF=1475483708; SCF=AvT6HCtAMdOj-c5qkVuiYsW5iilNltQh3db0hjO7i625C9Bz-SANrzU3iXo3gHwaBVv27vcf9rqEujv7jSm-Gzk.; SUB=_2A256zv0EDeTxGeNL7FUZ-CfJzT2IHXVWMINMrDV6PUJbktBeLWqskW0dWXcKG7NUc4iONSJ-bD2Dn1BYVQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MINdBKrimGBVg4AxBhZ3J5JpX5o2p5NHD95QfSKMN1hn4SKqpWs4Dqcjpi--fi-2Ei-2Ri--4iK.fiKLhi--fiK.fi-2ci--fiK.fi-2ci--fiK.fi-2cTK57e7tt; SUHB=0wnFlgOb05XDvk; SSOLoginState=1472892244'}
    is_find=False
    def get_page(self):
        url = 'http://login.weibo.cn/login/'
        try:
            req = urllib2.Request(url=url, headers=self.header)
            res = urllib2.urlopen(req)
            html = res.read().decode('utf-8')
            soup = bs4.BeautifulSoup(html, 'lxml')
            password = soup.find('input', type="password")['name']
            vk = soup.find(attrs={"name": "vk"})['value']
            capId = soup.find(attrs={"name": "capId"})['value']
            imglink = soup.find('img')['src']
            tempurl=soup.find('form')['action']
            logurl='http://login.weibo.cn/login/'+tempurl
            urllib.urlretrieve(imglink, '验证码.jpg')
            return password, vk, capId,logurl
        except URLError, e:
            if hasattr(e, 'reason'):
                print  e.reason
            elif hasattr(e, 'code'):
                print e.code


    def get_account(self):
        username = ""
        password = ""
        with open('account.txt', 'r') as f:
            flag = 0
            for line in f:
                if flag == 0:
                    username = line.strip()
                    flag += 1
                else:
                    password = line.strip()
        return username, password

    def get_login(self):
        passowrd_temp,vk,capId,logurl=self.get_page()
        code = raw_input("please input the code:")
        mobile,password=self.get_account()
        data={
            "mobile":mobile,
            "tryCount":"",
            "vk":vk,
            "capId":capId,
            "code":code,
            "backTtile":"http%3A%2F%2Fweibo.cn%2F",
            "backURL":"微博",
            "remember":"on",
            "submit":"登录"
        }
        data[passowrd_temp]=password
        data2=urllib.urlencode(data)
        try:
            filename='cookie.txt'
            req=urllib2.Request(url=logurl,headers=self.header)
            cookie= cookielib.MozillaCookieJar(filename)
            cookie_support = urllib2.HTTPCookieProcessor(cookie)
            opener = urllib2.build_opener(cookie_support)
            res=opener.open(req,data2)
            cookie.save(filename,ignore_discard=True,ignore_expires=True)
        except URLError,e:
            if hasattr(e,'reason'):
                print e.reason
            if hasattr(e,'code'):
                print e.code



    def get_opener(self):
        cj2=cookielib.MozillaCookieJar()
        cj2.load('cookie.txt',ignore_discard=True,ignore_expires=True)
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj2))
        return opener




    def get_user_json(self,page,pagebar,_rnd,userid):
        opener=self.get_opener()
        url="http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&pl_name=Pl_Official_MyProfileFeed__24&domain_op=100505&page="+page+"&pagebar="+pagebar+"&id=100505"+userid+"&script_uri=/u/"+userid+"&pre_page="+page+"&__rnd="+_rnd


    def get_mid_parse(self,omid,repost_list):
        for repost_item in repost_list:
            if int(repost_item['omid']) == int(omid):
                wbDetail = repost_item.find(attrs={"class": "WB_detail"})
                UserTemp = wbDetail.find(attrs={"node-type": "feed_list_item_date"})
                weiboLink = "http://weibo.com" + re.findall("(.*)\?from", UserTemp["href"])[0]
                weiboTime = UserTemp["title"]
                weiboUnixTime = UserTemp["date"]
                self.is_find = True
                return weiboLink, weiboTime, weiboUnixTime
            else:
                pass
    def search_mid(self,repost_list,omid,userid):
        weiboLink,weiboTime,weiboUnixTime=self.get_mid_parse(repost_list=repost_list,omid=omid)
        if self.is_find==False:
            for i in range(10000):
                page=i+1
                for j in range(2):
                    _rnd=j
                    timestr = str(time.time())
                    newtime = timestr.replace(".", "0")
                    temp_repost_list=self.get_user_json(page=i,pagebar=j,_rnd=newtime)
                    weiboLink, weiboTime, weiboUnixTime= self.get_mid_parse(omid=omid,repost_list=temp_repost_list)
                    return weiboLink,weiboTime,weiboUnixTime

        return weiboLink, weiboTime, weiboUnixTime










    def get_user_uid(self, link):
        opener = self.get_opener()
        req = urllib2.Request(link, headers=self.header)
        res = opener.open(req)
        html = res.read()
        # with open('userpage.html', 'w') as f:
        #     view = re.findall('<script>FM.view\((.*?)\)<\/script>', html)
        #     for i in view:
        #         s = json.loads(i)
        #         for b in s:
        #             if (isinstance(s[b], list)):
        #                 pass
        #             else:
        #                 f.write(s[b].encode('utf8'))
        self.html_parser(html)
        with open('test.html','r') as f2:
            temp=f2.read()
            temp_user_page=bs4.BeautifulSoup(temp,'lxml')
            userid_con=temp_user_page.find(attrs={"node-type":"focusLink"})
            userid=re.findall('uid=(.*?)&fnick',userid_con['action-data'])[0]
            return userid

    def html_parser(self,html):
        with open('test.html', 'w') as f:
            view = re.findall('<script>FM.view\((.*?)\)<\/script>', html)
            for i in view:
                s = json.loads(i)
                for b in s:
                    if (isinstance(s[b], list)):
                        pass
                    else:
                        f.write(s[b].encode("utf8"))

    def get_repost(self,user_link):
        opener=self.get_opener()
        req=urllib2.Request(user_link,headers=self.header)
        res=opener.open(req)
        html=res.read()
        self.html_parser(html)
        with open('test.html','r') as f1:

            temp=f1.read()

            html=bs4.BeautifulSoup(temp,'lxml',from_encoding="utf-8")
            repost_list=html.find_all(minfo=True)
            return repost_list
    def get_text(self,html):
        text_content=html.find(attrs={"node-type":"feed_list_reason"})
        text=text_content.get_text()
        return text

    def get_user(self,link):
            repost_list=self.get_repost(link)
            for html in repost_list:
                useridtemp = html
                userString=useridtemp['tbinfo']
                userid=re.findall('ouid=(.*)&rouid',userString)[0]
                usernameCon=html.find(attrs={'class':'WB_face'})
                originalUsernameTemp=html.find(attrs={'class':'WB_row_line WB_row_r4 clearfix S_line2'})
                originalUsername=re.findall('rootname=(.*)&rootuid',originalUsernameTemp.find_all('li')[1].find('a')['action-data'])[0]
                originalUid=re.findall('rootuid=(.*)&rooturl',originalUsernameTemp.find_all('li')[1].find('a')['action-data'])[0]
                originalLink=re.findall('rooturl=(.*)&url',originalUsernameTemp.find_all('li')[1].find('a')['action-data'])[0]
                username=usernameCon.find('a',attrs={"class":"W_face_radius"})["title"]
                timeCon1=html.find_all(attrs={'node-type':'feed_list_item_date'})[0]
                timeCon2=html.find_all(attrs={'node-type':'feed_list_item_date'})[1]
                userLinkTemp=timeCon1['href']
                weiboLink='http://weibo.com/'+re.findall('(.*\?)',userLinkTemp)[0]
                showtime=timeCon1['title']
                saveTime=timeCon1['date']
                originalShowTime=timeCon2['title']
                originalSaveTime=timeCon2['date']

                # print userid,username, showtime, saveTime,weiboLink
                linkList=weiboLinkList()
                tempNode=weiboNode(id=userid,name=username,link=weiboLink)
                tempNode.set_showTime(showtime=showtime)
                tempNode.set_unixTimeStamp(saveTime)
                linkList.append(tempNode)




                weiboParentArray=html.find_all(attrs={'extra-data':'type=atname'})
                for item in weiboParentArray:
                    parentUsername=re.findall('name=(.*)',item['usercard'])[0]
                    parentLink=re.findall('(.*)\?',item['href'])[0]
                    parentUserId=self.get_user_uid(parentLink)
                    parentTempNode=weiboNode(parentUserId,parentUsername,parentLink)
                    linkList.append(parentTempNode)
                    # print parentUserId,parentUsername,parentLink

                originalNode=weiboNode(originalUid,originalUsername,originalLink)
                originalNode.set_showTime(originalShowTime)
                originalNode.set_unixTimeStamp(originalSaveTime)
                linkList.append(originalNode)
                linkList.printAllLink()
                # print originalUid,originalUsername,originalShowTime,originalSaveTime, originalLink
                print "***************************************************************************"



wb=weiboLogin()
# wb.get_login()
wb.get_user('http://weibo.com/u/3627189164?profile_ftype=1&is_all=1#_0')




















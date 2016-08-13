
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


class weiboLogin:
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
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


    def get_opener(self):
        cj2=cookielib.MozillaCookieJar()
        cj2.load('cookie.txt',ignore_discard=True,ignore_expires=True)
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj2))
        return opener


    def get_user_uid(self, link):
        opener = self.get_opener()
        req=urllib2.Request(link,headers=self.header)
        res = opener.open(req)
        html = res.read()
        view=re.findall('<script>FM.view\((.*?)\)<\/script>',html)
        with open('view.html','w') as f:
            for i in view:
                r = i.encode('utf-8').decode('unicode_escape').encode('gbk')
                s = r.replace("\/", "/")
                f.write(s)
        with open('view.html','r') as f:
            newhtml=f.read()
            print newhtml

        # print bs4.BeautifulSoup(html,'lxml').find(attrs={'class':'btn_bed W_fl'})

        # return re.findall('uid=(.*)&fnick',bs4.BeautifulSoup(html,'lxml').find(attrs={'class':'btn_bed W_fl'})['action-data'])[0]
    def get_repost(self,user_link):
        opener=self.get_opener()
        req=urllib2.Request(user_link,headers=self.header)
        res=opener.open(req)
        html=res.read()
        with open('test.html', 'w') as f:
            view = re.findall('<script>FM.view\((.*?)\)<\/script>', html)
            for i in view:
               s=json.loads(i)
               for b in s:
                   if(isinstance(s[b],list)):
                       pass
                   else:
                       f.write(s[b].encode('utf8'))

             # r = i.decode('utf-8')
             # s=r.replace('\/','/')
             # print r
             # print s


            # s = r.replace("\/", "/")
            # print s
            # f.write(s)




    def get_user(self):
        with open('weiboExample.html','r') as f:
            temp=f.read()
            html=bs4.BeautifulSoup(temp,'lxml')
            useridtemp = html.find(attrs={'class':'WB_feed_type'})
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
            print userid,username, showtime, saveTime,weiboLink

            weiboParentArray=html.find_all(attrs={'extra-data':'type=atname'})
            for item in weiboParentArray:
                parentUsername=re.findall('name=(.*)',item['usercard'])[0]
                parentLink=re.findall('(.*)\?',item['href'])[0]
                print parentUsername,parentLink

            print originalUid,originalUsername,originalShowTime,originalSaveTime, originalLink





wb=weiboLogin()
wb.get_repost('http://weibo.com/u/3178295512?profile_ftype=1&is_all=1#_0')




















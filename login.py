# coding:utf-8
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
# 登陆微博
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
            # cj2=cookielib.MozillaCookieJar()
            # cj2.load('cookie.txt',ignore_discard=True,ignore_expires=True)
            # opener2=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj2))
            # req2=urllib2.Request('http://weibo.cn/?since_id=0&max_id=DDyTmzAV2&prev_page=1&page=2&vt=4',headers=self.header)
            # res2=opener2.open(req2)
            # html=res2.read()
            # print html
        except URLError,e:
            if hasattr(e,'reason'):
                print e.reason
            if hasattr(e,'code'):
                print e.code
    def get_user(self):


wb=weiboLogin()
wb.get_login()


















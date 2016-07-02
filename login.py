# coding:utf-8
import sys
import re
import bs4
import os
# import MySQLdb
import urllib
from urllib2 import HTTPError, URLError
import urllib2
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
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support)
    urllib2.install_opener(opener)

    def get_page(self):
        url = 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
        try:
            req = urllib2.Request(url=url, headers=self.header)
            res = urllib2.urlopen(req)
            html = res.read().decode('utf-8')
            soup = bs4.BeautifulSoup(html, 'lxml')
            password = soup.find('input', type="password")['name']
            vk = soup.find(attrs={"name": "vk"})['value']
            capId = soup.find(attrs={"name": "capId"})['value']
            imglink = soup.find('img')['src']
            urllib.urlretrieve(imglink, '验证码.jpg')
            return password, vk, capId
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

        # def start_login(self):
        # username,passowrd=self.get_account()
        # prepassowrd,vk,capId=self.get_page()
        # code=raw_input('请输入验证码:')
        # print code

        # data={
        #     'mobile':username,
        #     'code':code,
        #     'vk':vk,
        #     'capId':capId,
        #     'submit':'登录',
        #     'tryCount':'',
        #     'remember':'on',
        #     'backURL':'http%3A%2F%2Fweibo.cn%2F',
        #     'backTitle':'微博'
        # }
        # data[prepassowrd]=passowrd









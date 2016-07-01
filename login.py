# coding:utf-8
import sys
import re
import bs4
import urllib
import  urllib2
import json
import cookielib
# 登陆微博
class weiboLogin:
    cj=cookielib.LWPCookieJar()
    cookie_support=urllib2.HTTPCookieProcessor(cj)
    opener=urllib2.build_opener(cookie_support)
    urllib2.install_opener(opener)
    postdata={

    }

    def getpage(self):
        url='http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='


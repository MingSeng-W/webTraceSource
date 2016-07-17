# coding:utf-8
import re
import bs4
import os
import mysql.connector
import mysql
import urllib
import urllib2
import time

import cookielib
class weiboCrawlser:

    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support)
    urllib2.install_opener(opener)
    def connectMysql(self,username,userid,weibotext,weiboid):
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
        "INSERT INTO user(userid,username,weiboid,weibocontent) VALUES(%(userid)s,%(username)s,%(weiboid)s,%(weibocontent)s)")
        data_user = {
            'userid': userid,
            'username': username,
            'weiboid': weiboid,
            'weibocontent': weibotext
        }

        cursor.execute(add_user, data_user)
        conn.commit()
        cursor.close()
        conn.close()


    def test(self, pagenum,keyword):
        print 'downloading page' + str(pagenum)
        url = 'http://s.weibo.com/weibo/'+keyword+'&page=' + str(pagenum)
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Cookie': '_s_tentry=www.micmiu.com; Apache=2580452964109.3633.1468546273913; SINAGLOBAL=2580452964109.3633.1468546273913; ULV=1468546273941:1:1:1:2580452964109.3633.1468546273913:; SWB=usrmdinst_12; ALF=1471307009; SUB=_2A256jqBQDeTxGeNL7FUZ-CfJzT2IHXVWcMAYrDV8PUJbkNBeLUPykW1td6byhRAUKVh1YjwagX3FRd_sQg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MINdBKrimGBVg4AxBhZ3J5NHD95QfSKMN1hn4SKqpWs4Dqcjpi--fi-2Ei-2Ri--4iK.fiKLhi--fiK.fi-2ci--fiK.fi-2ci--fiK.fi-2cTK57e7tt; wvr=6; UOR=www.micmiu.com,widget.weibo.com,www.baidu.com; WBStore=8ca40a3ef06ad7b2|undefined'
        }
        req = urllib2.Request(url=url, headers=header)
        res = urllib2.urlopen(req)
        with open('test.html', 'w') as f:
            html = res.read()
            view = re.findall('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>', html)
            for i in view:
                # r = i.encode('utf-8').decode('unicode_escape').encode('utf-8')
                # s = r.replace("\/", "/")
                # f.write(s)
                print i


        with open('test.html', 'r') as f2:
            newthml = f2.read()
            newthmls = bs4.BeautifulSoup(newthml, 'lxml')
            imgAry = newthmls.find_all('img', attrs={'action-type': 'fl_pics'})
            print imgAry
            # 获取微博的用户名,微博id,用户名id,微博内容
            blogs = newthmls.find_all(attrs={'action-type': 'feed_list_item'})
            for i in range(0, len(blogs)):
                temp = blogs[i].find(attrs={'class': 'W_texta W_fb'})
                username = temp['nick-name']
                useridLink = temp['href']
                weiboText = blogs[i].find(attrs={'class': 'comment_txt'}).get_text().strip()
                weiboId = re.findall('refer_flag=(.*)', useridLink)[0]
                try:
                    userid = re.findall('http:\/\/weibo.com\/u\/(.*?)\?', useridLink)[0]
                    self.connectMysql(username,userid,weiboText,weiboId)
                    # print userid, username, weiboId, weiboText
                except:
                    useridtemp = re.sub(r'http://weibo.com/(.*?)', '', useridLink)
                    useridtemp2 = re.sub('/?refer_flag', '', useridtemp)
                    userid = re.findall(r'(^\w*)', useridtemp2)[0]
                    # print userid, username, weiboId, weiboText
            path = os.path.abspath('.')
            imgpath = path + '/images/'
            totalImageNum = int([len(files) for root, dirs, files in os.walk(imgpath)][0])
            for index in range(0, len(imgAry)):
                imglink = imgAry[index]['src']
                imgname = './images/' + str(index + totalImageNum) + '.jpg'
                urllib.urlretrieve(imglink, imgname)
            print 'finsh download page' + str(pagenum)



def connectMysql(username,userid,weibotext,weiboid):
    config={
        'user':'root',
        'password':'',
        'host':'localhost',
        'port':'3306',
        'database':'weibostore'
    }
    conn=mysql.connector.connect(**config)
    cursor=conn.cursor()
    add_user=("INSERT INTO user(userid,username,weiboid,weibocontent) VALUES(%(userid)s,%(username)s,%(weiboid)s,%(weibocontent)s)")
    data_user={
        'userid':userid,
        'username':username,
        'weiboid':weiboid,
        'weibocontent':weibotext
    }

    cursor.execute(add_user,data_user)
    conn.commit()
    result_set=cursor.fetchone()
    print result_set
    cursor.close()
    conn.close()






keyword=raw_input("please in put the keyword:")
wb = weiboCrawlser()
for i in range(1, 7):
    wb.test(i,keyword)
    time.sleep(20)
print 'finish all'


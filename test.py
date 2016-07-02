# coding:utf-8
import re
import bs4
import os
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

    def test(self, pagenum):
        print 'downloading page' + str(pagenum)
        url = 'http://s.weibo.com/weibo/sss&page=' + str(pagenum)
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Cookie': 'SINAGLOBAL=7794664723802.307.1464800947011; _s_tentry=-; Apache=8258607474181.003.1467273666438; ULV=1467273666448:5:5:2:8258607474181.003.1467273666438:1467262664430; SWB=usrmdinst_14; NSC_wjq_txfjcp_mjotij=ffffffff094113d645525d5f4f58455e445a4a423660; UOR=www.liaoxuefeng.com,widget.weibo.com,www.baidu.com; appkey=; WBtopGlobal_register_version=c5a1a241471e96ea; SUB=_2A256cgCoDeTxGeNL7FUZ-CfJzT2IHXVZBnVgrDV8PUJbmtBeLWLEkW8g9LCVu3mmtEhqMNpCWlKRFm8QSA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MINdBKrimGBVg4AxBhZ3J5JpX5K2hUgL.Fo-fS0MR1h.fSo22dJLoI02LxK-LBKzLBKnLxK.L1K-L1-eLxK-L1K-LBKqLxK-L1K-LBKqLxK-L1K-LBKq_eh50; SUHB=0OMUZMcoeOe70z; SSOLoginState=1467379960; un=15520441791; WBStore=8ca40a3ef06ad7b2|undefined'
        }
        req = urllib2.Request(url=url, headers=header)
        res = urllib2.urlopen(req)
        with open('test.html', 'w') as f:
            html = res.read()
            view = re.findall('<script>STK && STK.pageletM && STK.pageletM.view\((.*?)\)<\/script>', html)
            for i in view:
                r = i.encode('utf-8').decode('unicode_escape').encode('utf-8')
                s = r.replace("\/", "/")
                f.write(s)

        with open('test.html', 'r') as f2:
            newthml = f2.read()
            newthmls = bs4.BeautifulSoup(newthml, 'lxml')
            imgAry = newthmls.find_all('img', attrs={'action-type': 'fl_pics'})
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
                    print userid, username, weiboId, weiboText
                except:
                    useridtemp = re.sub(r'http://weibo.com/(.*?)', '', useridLink)
                    useridtemp2 = re.sub('/?refer_flag', '', useridtemp)
                    userid = re.findall(r'(^\w*)', useridtemp2)[0]
                    print userid, username, weiboId, weiboText
            path = os.path.abspath('.')
            imgpath = path + '/images/'
            totalImageNum = int([len(files) for root, dirs, files in os.walk(imgpath)][0])

            for index in range(0, len(imgAry)):
                imglink = imgAry[index]['src']
                imgname = './images/' + str(index + totalImageNum) + '.jpg'
                urllib.urlretrieve(imglink, imgname)
            print 'finsh download page' + str(pagenum)


wb = weiboCrawlser()
for i in range(1, 3):
    wb.test(i)
    time.sleep(10)
print 'finish all'


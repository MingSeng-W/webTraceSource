## 数据库的设计
数据库表的设计:
关于新浪微博溯源的主要有博主的名称,博主的id,微博的id,他的父节点的微博id,和他的子节点的微博id,时间,转发量,主页链接


爬取方法:
1.给定微博,首先判断改微博是否为转发的微博,如果是的话,那么就进行下一步的解析;如果不是的话,那么就丢弃
判断微博是否为转发的算法:
    1判断用户的转发消息中是否有@,然后进行取舍

   try:
        next=div.contians('@')
        print "this is a repost weibo"
   except:
         print 'this is a original weibo'

2.分析微博的结构,找出weibo的id,现在转发weibo博主的id,用户名,爬取的上一个博主的id,用户名,最后再查出来源博主的微博.



### 2016/9/11日,获得最后的时间
1.首先获得搜索的关键词检索出来的关键词,的totalpage
2.跳到totalpage的那一页,找出最后的时间
3.判读totalpage的页数是否为50页,如果为50页,那么就拿到时间,然后,做一个以时间为关键词的搜索
4.这时候应该设置一个flag,判断flag,得到循环结束的条件


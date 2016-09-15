# coding:utf-8

from __future__ import division
import jieba
import jieba.analyse
sentence="最担心的事情发生了：男子手机掉厕所伸手去掏 手卡厕所一整夜[doge]】14日早上6点许，惠州市消防员接到报警称，一居民楼有人被困厕所。被困人说，自己半夜2点多起来上厕所，不小心手机就掉进了厕所，因为家里没其它人，就被卡了一晚上，幸好早上邻居醒来听到了他的呼救声，才帮忙报警。最终消防员将厕所盆破拆，才将人救出。"
sentence2="【最担心的事情发生了：男子手机掉厕所伸手去掏 手卡厕所一整夜[doge]】14日早上6点许，惠州市消防员接到报警称，一居民楼有人被困厕所。被困人说，自己半夜2点多起来上厕所，不小心手机就掉进了厕所，因为家里没其它人，就被卡了一晚上，幸好早上邻居醒来听到了他的呼救声，才帮忙报警。最终消防员将厕所盆破拆，才将人救出"
tags2=jieba.lcut_for_search(sentence)
seg=3.674
topk1=int((len(sentence)/3)/seg)
topk2=int(len(sentence2)/3/seg)
tags=jieba.analyse.extract_tags(sentence=sentence,topK=topk1,withWeight=False,allowPOS=())
tags3=jieba.analyse.extract_tags(sentence=sentence2,topK=topk2,withWeight=False,allowPOS=())
mystr=""


# print int(len(sentence)/3)
print " ".join(tags)
print " ".join(tags3)
k=0
print (len(set(tags)))
diff=list(set(tags3).intersection((set(tags))))
k= len(diff)
print k

len1=len(set(tags))
len2=len(set(tags3))
myfloat=(len1)/(len2)
result=(k/len1)*myfloat*100

print "%.2f%%"%result




# 关于文本相似度的想法:
# 1.提取关键词,然后放入list里面对其进行对比
# 2.做出余弦向量
# 3.反复测试
# 由于微博属于短文本,每个词的词频都是0,1之类的构建为余
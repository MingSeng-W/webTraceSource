# coding:utf-8

from __future__ import division
import jieba
import jieba.analyse
import re

class TextSimlar(object):

    def getResult(self,sentence,sentence2):
        sentence=self.prepare(sentence)
        sentence2=self.prepare(sentence2)
        tags2=jieba.lcut_for_search(sentence)
        seg=3.674
        topk1=int((len(sentence)/3)/seg)
        topk2=int(len(sentence2)/3/seg)
        tags=jieba.analyse.extract_tags(sentence=sentence,topK=topk1,withWeight=False,allowPOS=())
        tags2=jieba.analyse.extract_tags(sentence=sentence2,topK=topk2,withWeight=False,allowPOS=())
        # 集合求交集
        diff=list(set(tags2).intersection((set(tags))))
        k= len(diff)
        len1=len(set(tags))
        len2=len(set(tags2))
        # 倍数乘积
        myfloat=(len1)/(len2)
        result=(k/len1)*myfloat*100
        return result

    def getSearchWord(self,sentence):

        result=jieba.analyse.extract_tags(sentence=sentence,topK=4)
        result=" ".join(result)
        return result

    def prepare(self,sentence):
        sentence=self.replaceToken("，",sentence)
        sentence = self.replaceToken("……", sentence)
        sentence=self.replaceToken("。",sentence)
        sentence=self.replaceToken("：",sentence)
        sentence=self.replaceToken("（",sentence)
        sentence=self.replaceToken("）",sentence)
        sentence=self.replaceToken("【",sentence)
        sentence=self.replaceToken("】",sentence)
        sentence=self.replaceToken("！",sentence)
        sentence=self.replaceToken('"',sentence)
        sentence=self.replaceToken('[',sentence)
        sentence=self.replaceToken(']',sentence)
        sentence=self.replaceToken('#',sentence)
        sentence=self.replaceToken('；',sentence)
        sentence=self.replaceToken('http',sentence)
        sentence=self.replaceToken('cn',sentence)
        return sentence

    def replaceToken(self,token,sentence):
        return sentence.replace(token,"")
        return sentence

# print test.getSearchWord("")




# 关于文本相似度的想法:
# 1.提取关键词,然后放入list里面对其进行对比
# 2.做出余弦向量
# 3.反复测试
# 由于微博属于短文本,每个词的词频都是0,1之类的构建为余
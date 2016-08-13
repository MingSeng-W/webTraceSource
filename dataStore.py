# coding:utf-8

class weiboNode(object):

    def __init__(self,id,name,link):
        self.name=name
        self.id=id
        self.link=link
        self.unixTimeStamp=0
        self.parent=None
        self.showTime=""


    def set_unixTimeStamp(self,unixTimeStamp):
        self.unixTimeStamp=unixTimeStamp

    def set_parant(self,parent):
        self.parent=parent
    def set_showTime(self,showtime):
        self.showTime


class weiboLinkList(object):

    def __init__(self):
        self.head=None


    def get_length(self):
        p=self.head
        length=0
        while p!=None:
            length+=1
            p=p.parent
        return length

    def append(self,node):
        if self.head==None:
            self.head=node
        else:
            p=self.head
            while p.parent!=None:
                p=p.parent
            p.parent=node

    def printAllLink(self):
        p=self.head
        while p!=None:
            if p.parent!=None:
                print p.name, "--->"
            else:
                print p.name
            p=p.parent















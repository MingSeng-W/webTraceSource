# coding:utf-8
import time
import urllib
def timeCaclulate(UnixTime1):
    UnixTime1=dateTime_unixTime(UnixTime1)
    UnixTime2=currentTime()
    timetemp=int((UnixTime1+UnixTime2)/2)
    return unix_dateTime(timetemp)

def timeSlace(s):
    temp=time.strptime(s,"%Y-%m-%d %H:%M:%S")
    Y,m,d,H,M=temp[0:5]
    return str(Y)+'-'+str(m)+'-'+str(d)+' '+str(H)+":"+str(M)

def currentTime():
    return  int(time.time())


def dateTime_unixTime(timestr):
    timestr=timestr+':34'
    s=time.mktime(time.strptime(timestr,"%Y-%m-%d %H:%M:%S"))
    return int(s)


def unix_dateTime(UnixTime):
    s=time.localtime(UnixTime)
    return time.strftime("%Y-%m-%d %H:%M:%S",s)













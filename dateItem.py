# coding:utf-8

import mysql.connector
import mysql

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': '3306',
    'database': 'weibostore'
}


def connectMysql(username, link, weibotext, time, date, myindex, similar,topic):

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    add_user = (
        "INSERT INTO user(username,link,weibotext,time,date,myindex,similar,topic) VALUES(%(username)s,%(link)s,%(weibotext)s,%(time)s,%(date)s,%(myindex)s,%(similar)s,%(topic)s)")
    data_user = {
        'username': username,
        'weibotext': weibotext,
        'time': time,
        'date': date,
        'link': link,
        'myindex': str(myindex),
        'similar': str(similar),
        'topic':topic
    }
    cursor.execute(add_user, data_user)
    conn.commit()
    cursor.close()
    conn.close()

def getDataBaseIndex(tableName):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query= "SELECT * FROM "+tableName
    count=cursor.execute(query)
    data=cursor.fetchall()
    length=len(data)
    conn.close()
    return length




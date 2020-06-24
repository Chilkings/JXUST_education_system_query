#!/usr/bin/python 
# -*- coding: utf-8 -*-

import time
import requests
import re
import os
import json
import datetime

# 强智教务管理系统
########################################
account = ""       #填入一卡通号
password = ""      #填入教务系统密码
url = "http://jw.jxust.edu.cn/app.do" 
########################################


class SW(object):
    """docstring for SW"""
    def __init__(self, account, password,url):
        super(SW, self).__init__()
        self.url = url
        self.account = account
        self.password = password
        self.session = self.login()
    
    HEADERS = {
        "User-Agent":"Mozilla/5.0 (Linux; U; Mobile; Android 6.0.1;C107-9 Build/FRF91 )",
        "Referer": "http://www.baidu.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2",
        "cache-control": "max-age=0"
    }

    def login(self):
        params={
            "method" : "authUser",
            "xh" : self.account,
            "pwd" : self.password
        }
        session = requests.Session()
        req = session.get(self.url, params=params,timeout = 5,headers = self.HEADERS)
        s = json.loads(req.text)
        print(s)
        # if s['flag'] != "1" : exit(0)
        self.HEADERS['token'] = s['token']
        return session

    

    def get_handle(self,params):
        req = self.session.get(self.url ,params = params ,timeout = 5 ,headers=self.HEADERS)
        return req

    def get_student_info(self):
        params = {
            "method" : "getUserInfo",
            "xh" : self.account
        }
        req = self.get_handle(params)
        print(req.text)
    
    def get_current_time(self):
        params = {
            "method" : "getCurrentTime",
            "currDate" : datetime.datetime.now().strftime('%Y-%m-%d')
        }
        req = self.get_handle(params)
        print(req.text)
        return req.text

    def get_class_info(self,zc = -1):
        s = json.loads(self.get_current_time())
        params={
            "method" : "getKbcxAzc",
            "xnxqid" : s['xnxqh'],
            "zc" : s['zc'] if zc == -1 else zc,
            "xh" : self.account
        }
        req = self.get_handle(params)
        print(req.text)

    def get_classroom_info(self,idleTime = "allday"):
        params={
            "method" : "getKxJscx",
            "time" : datetime.datetime.now().strftime('%Y-%m-%d'),
            "idleTime" : idleTime
        }
        req = self.get_handle(params)
        print(req.text)

    def get_grade_info(self,sy = "",xh = ""):
        params={
        "method" : "getCjcx",
        "xh" : self.account,
        "xnxqid" : sy
        }
        req = self.get_handle(params)
        print("全部成绩" if sy == "" else sy)
        s = json.loads(req.text)
        if s['success'] == True :
            for x in s['result']:
                print("%s  %s   %d   %s" % (x['xm'],str(x['zcj']),x['xf'],x['kcmc']))
        else : 
            print("空")

    def get_exam_info(self):
        params={
            "method" : "getKscx",
            "xh" : self.account,
        }
        req = self.get_handle(params)
        print(req.text)




if __name__ == '__main__':
    Q = SW(account,password,url)
    # Q.get_student_info() #获取学生信息
    # Q.get_current_time() #获取学年信息
    # Q.get_class_info() #当前周次课表
    # Q.get_class_info(3) #指定周次课表
    # Q.get_classroom_info("0102") #空教室查询 "allday"：全天 "am"：上午 "pm"：下午 "night"：晚上 "0102":1.2节空教室 "0304":3.4节空教室
    # Q.get_grade_info("2019-2020-2","242018xxxx") # 成绩查询 # 传入参数为学年以及一卡通号
    # Q.get_exam_info() #获取考试信息

    #一次性查询本班的成绩
    # for i in range(242018xxxx,242018xxxx):
    #      Q.get_grade_info("2019-2020-2",i)



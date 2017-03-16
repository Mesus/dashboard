#coding:utf8
#物流

from flask import Blueprint, render_template
from app.models import dbsession,logistics
from sqlalchemy import func
from app.config import *
import sys,datetime

logi = Blueprint('logistics', __name__)

def logi_up(time):
    dic = {}
    rc = dbsession.query(logistics).filter(logistics.data_time.like('%'+time+'%')).count()
    if rc > 0:
        for row in dbsession.query(func.sum(logistics.cc),func.sum(logistics.ccl),func.sum(logistics.cql)).filter(logistics.data_time.like('%'+time+'%')):
            print row
            dic['cc'] = row[0] if row[0]!=None else 0
            dic['ccl'] = row[1] if row[1]!=None else 0
            dic['cql'] = row[2] if row[2]!=None else 0
    print dic
    return dic
def logi_trend(time,dic):
    # d1 = datetime.datetime.now()
    d1 = datetime.datetime.strptime(time, "%Y%m%d").date()
    d3 = d1 + datetime.timedelta(days=-1)
    sDate = str(d3).replace('-','')
    print sDate
    dic_y = logi_up(sDate)
    return compare(dic_y,dic)

def compare(dic_y,dic):
    t = []
    if len(dic)==0 or len(dic_y)==0:
        ns = getConfig('trendIcon','none')
        for i in range(6):
            t.append(ns)
    else:
        t.append(ternary(dic['cc'],dic_y['cc']))
        t.append(ternary(dic['ccl'],dic_y['ccl']))
        t.append(ternary(dic['cql'],dic_y['cql']))

    print t
    return t
def ternary(t,y):
    result = ''
    if t > y:
        result = getConfig('trendIcon','gain')
    elif t < y:
        result = getConfig('trendIcon','decline')
    else:
        result = getConfig('trendIcon','leveloff')
    return result

def control(time):
    dic = {}
    rc = dbsession.query(logistics).filter(logistics.data_time.like('%'+time+'%')).count()
    if rc > 0:
        for row in dbsession.query(func.sum(logistics.gk_wd),func.sum(logistics.gk_dp)).filter(logistics.data_time.like('%'+time+'%')):
            print row
            dic['wd'] = row[0] if row[0]!=None else 0
            dic['dp'] = row[1] if row[1]!=None else 0
    return dic
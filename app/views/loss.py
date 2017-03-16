#coding:utf8
#损耗

from flask import Blueprint, render_template,request
from app.models import dbsession,li,lp,la
from sqlalchemy import func
from app.config import *
import datetime

loss = Blueprint('loss', __name__)

def loss_up(time):
    dic = {}
    print time
    rc = dbsession.query(li).filter(li.insert_time.like('%'+time+'%')).count()
    if rc > 0:
        for row in dbsession.query(func.sum(li.number)).filter(li.insert_time.like('%'+time+'%'),li.type==0):
            print row[0]
            dic['yqshl'] = row[0]

        for row1 in dbsession.query(func.sum(lp.number)).filter(lp.insert_time.like('%'+time+'%'),lp.type==0):
            print row1[0]
            dic['jgshl'] = row1[0] if row1[0]!=None else 0
        # #
        for row2 in dbsession.query(func.sum(la.number)).filter(la.insert_time.like('%'+time+'%'),la.type==0):
            print row2[0]
            dic['dbshl'] = row2[0] if row2[0]!=None else 0

    print dic
    return dic
def loss_trend(time,dic):
    # d1 = datetime.datetime.now()
    d1 = datetime.datetime.strptime(time, "%Y%m%d").date()
    d3 = d1 + datetime.timedelta(days=-1)
    sDate = str(d3).replace('-','')
    print sDate
    dic_y = loss_up(sDate)
    return compare(dic_y,dic)

def compare(dic_y,dic):
    t = []
    if len(dic)==0 or len(dic_y)==0:
        ns = getConfig('trendIcon','none')
        for i in range(6):
            t.append(ns)
    else:
        t.append(ternary(dic['yqshl'],dic_y['yqshl']))
        t.append(ternary(dic['jgshl'],dic_y['jgshl']))
        t.append(ternary(dic['dbshl'],dic_y['dbshl']))

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

@loss.route('/loss_index')
def index():
    sTime = request.args.get('time')
    loss = loss_up(sTime)
    lt = loss_trend(sTime,loss)
    if len(loss)==0 :
        loss = {'yqshl':0,'jgshl':0,'dbshl':0}
    return render_template('loss/page_sh.html',yyy=loss['yqshl'],jgshl=loss['jgshl'],dbshl=loss['dbshl'])
if __name__=='__main__':
    time = '20160407'
    area = u'成都'
    loss_up(time,area)
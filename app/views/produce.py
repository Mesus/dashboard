#coding:utf8
#生产

from flask import Blueprint, render_template,session,request,jsonify
from app.models import dbsession,product
from sqlalchemy import func
from app.config import *
import datetime,time


produce_br = Blueprint('produce_br', __name__)

#生产量上半部分数据层
def product_up(time):
    dic = {}
    rc = dbsession.query(product).filter(product.data_time.like('%'+time+'%')).count()
    if rc > 0:
        for row in dbsession.query(func.sum(product.ckl),func.sum(product.csl),func.sum(product.jpckc),func.sum(product.spckc),func.sum(product.yjccl)).filter(product.data_time.like('%'+time+'%')):
            print row
            dic['ckl'] = row[0] if row[0]!=None else 0
            dic['csl'] = row[1] if row[1]!=None else 0
            dic['jpckc'] = row[2] if row[2]!=None else 0
            dic['spckc'] = row[3] if row[3]!=None else 0
            dic['yjccl'] = row[4] if row[4]!=None else 0
    print dic
    return dic

#生产量上半部分数据趋势图标
def product_trend(time,dic):
    # d1 = datetime.datetime.now()
    d1 = datetime.datetime.strptime(time, "%Y%m%d").date()
    d3 = d1 + datetime.timedelta(days=-1)
    sDate = str(d3).replace('-','')
    print sDate
    dic_y = product_up(sDate)
    return compare(dic_y,dic)

#数据趋势的比较方法
def compare(dic_y,dic):
    t = []
    if len(dic)==0 or len(dic_y)==0:
        ns = getConfig('trendIcon','none')
        for i in range(6):
            t.append(ns)
    else:
        t.append(ternary(dic['csl'],dic_y['csl'],'b'))
        t.append(ternary(dic['ckl'],dic_y['ckl'],'s'))
        # t.append(ternary(dic['csl'],dic_y['csl'],'s'))
        t.append(ternary(dic['jpckc'],dic_y['jpckc'],'s'))
        t.append(ternary(dic['spckc'],dic_y['spckc'],'s'))
        t.append(ternary(dic['yjccl'],dic_y['yjccl'],'s'))

    print t
    return t

#数据趋势图标
def ternary(t,y,l):
    result = ''
    if t > y:
        result = getConfig('trendIcon','gain')
    elif t < y:
        result = getConfig('trendIcon','decline')
    else:
        result = getConfig('trendIcon','leveloff')
    return result

#生产量下半部分chart
def product_down(param,type,cdate):
    # now = datetime.datetime.now()
    # cdate = str(now)[0:10].replace('-','')
    now = datetime.datetime.strptime(cdate, "%Y%m%d").date()
    where = "data_time like '%"+cdate+"%'"
    if param == 'month':
        cdate = cdate[0:6]
        where = "data_time like '%"+cdate+"%'"
    elif param == 'week':
        cw = now.weekday()
        mon = now + datetime.timedelta(days=-cw)
        sun = mon + datetime.timedelta(days=+6)
        monday = str(mon)[0:10].replace('-','')+'00'
        sunday = str(sun)[0:10].replace('-','')+'24'
        print monday
        print sunday
        where = "data_time>='"+monday+"' and data_time<='"+sunday+"'"

    print cdate
    categories = ''
    series = ''
    if param == 'all' or param == 'day':
        for row in dbsession.query(product.pl,'sum('+type+')').filter(where).group_by(product.pl):
            categories += "'"+row[0]+"',"
            series += str(row[1])+','
    else:
        for row in dbsession.query(product.pl,'sum('+type+')').filter(where).group_by(product.pl):
            categories += "'"+row[0]+"',"
            series += str(row[1])+','

    categories = categories[:len(categories)-1]
    series = series[:len(series)-1]
    print categories
    print series
    return categories,series

#api响应
@produce_br.route('/product_index')
def index():
    re_param = request.args.get('param')
    if not re_param:
        re_param = 'all'

    re_type = request.args.get('type')
    if not re_type:
        re_type = 'product.csl'
    else:
        re_type = 'product.'+re_type

    cdate = request.args.get('time')
    if not cdate:
        sTime = time.strftime('%Y%m%d', time.localtime(time.time()))

    p = session['product']
    pt = session['product_trend']

    pd = product_down(re_param,re_type,cdate)
    cate = '['+pd[0]+']'
    ser = '['+pd[1]+']'
    return render_template('produce/page_csl.html',csl=p['csl'],
                           ckl=p['ckl'],jpckc=p['jpckc'],
                           spckc=p['spckc'],yjccl=p['yjccl'],
                           pt0=pt[0],pt1=pt[1],pt2=pt[2],pt3=pt[3],pt4=pt[4],categories=cate,series=ser)

#chart ajax响应
@produce_br.route('/product_chart')
def chart():
    re_param = request.args.get('param')
    if not re_param:
        re_param = 'all'

    re_type = request.args.get('type')
    if not re_type:
        re_type = 'product.csl'
    else:
        re_type = 'product.'+re_type

    cdate = request.args.get('time')
    if not cdate:
        sTime = time.strftime('%Y%m%d', time.localtime(time.time()))

    print '&&&&&&&&',re_param,re_type,cdate
    pd = product_down(re_param,re_type,cdate)
    return jsonify(categories=pd[0].replace("'",""),series=pd[1])

if __name__=='__main__':
    # time = '20160512'
    # dic = product_up(time,'')
    # product_trend(time,dic,'')
    product_down('all','product.ckl')
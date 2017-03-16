#coding:utf8
#销售

from flask import Blueprint, render_template,request
from app.models import dbsession,pm,sell_t
from sqlalchemy import func
import sys,datetime
from app.config import *
import vis

sell = Blueprint('sell', __name__)

@sell.route('/tts')
def trace_the_source():
    name = request.args.get('name')

    name = sys.path[0]+'/app/static/tts/'+name+'.js'
    file_object = open(name)
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close( )
    return render_template('sell/hie.html',js=all_the_text)

@sell.route('/bundle')
def bund():
    return render_template('sell/bundle.html')

@sell.route('/snap')
def snap():
    return render_template('sell/snap.html')

@sell.route('/trace_index/<filename>')
def sell_trace_index(filename):
    # tag = ''
    # for mc in dbsession.query(pm.pmmc):
    #     tag += '''<a class="tag" target="_blank" href="">%s</a>'''%(mc[0])
    #     # print tag
    v = vis.CreateVis()
    sc = v.create(filename)
    g = v.group(filename)
    return render_template('sell/ontology.html',code=sc,g1=g[0],g2=g[1],g3=g[2],g4=g[3],g5=g[4])

@sell.route('/sell_index')
def index():

    return render_template('sell/page_xsl.html')

def sell_up(time):
    dic = {}
    rc = dbsession.query(sell_t).filter(sell_t.data_time.like('%'+time+'%')).count()
    if rc > 0:
        for row in dbsession.query(func.sum(sell_t.xsl),func.sum(sell_t.kgl),func.sum(sell_t.dbl)).filter(sell_t.data_time.like('%'+time+'%')):
            print row
            dic['xsl'] = row[0] if row[0]!=None else 0
            dic['kgl'] = row[1] if row[1]!=None else 0
            dic['dbl'] = row[2] if row[2]!=None else 0
    print dic
    return dic

def sell_trend(time,dic):
    # d1 = datetime.datetime.now()
    d1 = datetime.datetime.strptime(time, "%Y%m%d").date()
    d3 = d1 + datetime.timedelta(days=-1)
    sDate = str(d3).replace('-','')
    print sDate
    dic_y = sell_up(sDate)
    return compare(dic_y,dic)

def compare(dic_y,dic):
    t = []
    if len(dic)==0 or len(dic_y)==0:
        ns = getConfig('trendIcon','none')
        for i in range(6):
            t.append(ns)
    else:
        t.append(ternary(dic['xsl'],dic_y['xsl']))
        t.append(ternary(dic['kgl'],dic_y['kgl']))
        t.append(ternary(dic['dbl'],dic_y['dbl']))

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

if __name__=='__main__':
    # sell_trace_index()
    sell_up('20160407')
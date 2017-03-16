#coding:utf8
from flask import request,Blueprint,render_template,session
from views.produce import product_up,product_trend
from views.sell import sell_up,sell_trend
from views.loss import loss_up,loss_trend
from views.logistics import logi_up,logi_trend,control
from views.weather import allWeather,query_main_brief
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
profile = Blueprint('profile', __name__)


@profile.route('/')
def index():
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    sTime = request.args.get('time')
    if not sTime:
        sTime = today
    print sTime

    #生产
    print '***************product'
    product = product_up(sTime)
    pt = product_trend(sTime,product)
    if len(product)==0 :
        product = {'csl':0,'ckl':0,'jpckc':0,'spckc':0,'yjccl':0}

    #销售
    print '***************sell'
    sell = sell_up(sTime)
    st = sell_trend(sTime,sell)
    if len(sell) == 0:
        sell = {'xsl':0,'kgl':0,'dbl':0}

    #损耗
    print '***************loss'
    loss = loss_up(sTime)
    lt = loss_trend(sTime,loss)
    if len(loss)==0 :
        loss = {'yqshl':0,'jgshl':0,'dbshl':0}

    #物流
    print '***************logi'
    logi = logi_up(sTime)
    logint = logi_trend(sTime,logi)
    if len(logi)==0 :
        logi = {'cc':0,'ccl':0,'cql':0}

    #气象
    print '***************weather'
    # allWeather(today)
    w = query_main_brief(sTime)
    print w

    #Control
    ctrl = control(sTime)
    if len(ctrl)==0 :
        ctrl = {'wd':0,'dp':0}

    #session
    pro = {'csl':str(product['csl']),'ckl':str(product['ckl']),'jpckc':str(product['jpckc']),'spckc':str(product['spckc']),'yjccl':str(product['yjccl'])}
    session['product'] = pro
    session['product_trend'] = pt
    return render_template("main/main.html",csl=product['csl'],
                           ckl=product['ckl'],jpckc=product['jpckc'],
                           spckc=product['spckc'],yjccl=product['yjccl'],
                           pt0=pt[0],pt1=pt[1],pt2=pt[2],pt3=pt[3],pt4=pt[4],xsl=sell['xsl'],kgl=sell['kgl'],dbl=sell['dbl'],st0=st[0],st1=st[1],st2=st[2],
                           yqshl=loss['yqshl'],jgshl=loss['jgshl'],
                           dbshl=loss['dbshl'],lt0=lt[0],lt1=lt[1],lt2=lt[2],cc=logi['cc'],ccl=logi['ccl'],cql=logi['cql'],logint0=logint[0],logint1=logint[1],logint2=logint[2],d_icon=w[0],d_desc=w[1],d_temp=w[2],temp=w[3],desc=w[4],cnname=w[5],wd=ctrl['wd'],dp=ctrl['dp'])
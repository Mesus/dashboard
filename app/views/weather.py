# coding:utf8
#气象

from flask import Blueprint, render_template,request
import urllib,sys,re
from app.models import weather_detail,dbsession
from weather_dic import *
import time

weather_br = Blueprint('weather', __name__)

today = time.strftime('%Y%m%d', time.localtime(time.time()))

@weather_br.route('/weather_index')
def index():
    today = request.args.get('time')
    l = query_index_brief(today)
    c = locals()
    j = 0
    print j
    for i in range(0,10):
        print l[j]
        c['c'+str(i)+'_name'] = l[j]
        c['c'+str(i)+'_icon'] = l[j+1]
        c['c'+str(i)+'_qx'] = l[j+2]
        c['c'+str(i)+'_fl'] = l[j+3]
        c['c'+str(i)+'_wd'] = l[j+4]
        c['c'+str(i)+'_fx'] = l[j+5]
        c['c'+str(i)+'_desc'] = l[j]
        j += 6
    print c
    return render_template('weather/page_nc.html',**c)

@weather_br.route('/weather_detail/<desc>/<ut>')
def detail(desc,ut):
    print 'detail:'+desc
    l = query_detail(desc,ut)

    c = locals()
    c['c_0_name'] = l[0]
    j = 0
    for i in range(0,7):
        print l[j]
        if i== 0:
            j += 1
        c['c_'+str(i)+'_day'] = l[j]
        c['c_'+str(i)+'_week'] = l[j+1]
        c['c_'+str(i)+'_icon'] = l[j+2]
        c['c_'+str(i)+'_qx'] = l[j+3]
        c['c_'+str(i)+'_wd'] = l[j+4]
        c['c_'+str(i)+'_fx'] = l[j+5]
        c['c_'+str(i)+'_fl'] = l[j+6]
        j = j+6+1
    query_chart(desc,c)
    print c
    return render_template('weather/page_qx.html',**c)

def query_chart(desc,c):
    # d = locals()
    rst = dbsession.query(weather_detail.w_detail).filter(weather_detail.w_area==desc,weather_detail.w_time==today)
    for row in rst:
        i = 0
        for bits in row[0].split('|'):
            j = 0
            for plot in bits.split(','):
                c['d_'+str(i)+'_'+str(j)] = plot
                j += 1
            i += 1

def query_detail(desc,ut):
    l = []
    rst = dbsession.query(weather_detail.w_area,weather_detail.d_one,
                    weather_detail.d_two,weather_detail.d_three,
                    weather_detail.d_four,weather_detail.d_five,
                    weather_detail.d_six,weather_detail.d_seven).filter(weather_detail.w_area==desc,weather_detail.w_time==ut)
    for row in rst:
        print len(row)
        l.append(row[0])
        i = 1
        for arr in range(1,len(row)):
            arr = row[i].split(",")
            l.append(arr[0])# 哪天
            l.append(arr[1])#星期几
            l.append(wdesc[arr[2]])# 天气图标
            l.append(arr[2])# 天气情况
            l.append(arr[3])# 温度
            l.append(arr[4])#风向
            l.append(arr[5])#风力
            i += 1
    print l
    return l
def query_index_brief(time):
    l = []
    rst = dbsession.query(weather_detail.w_area,weather_detail.d_one).filter(weather_detail.w_time==time)
    for row in rst:
        l.append(row[0])
        arr = row[1].split(',')
        l.append(wdesc[arr[2]])
        l.append(arr[2])
        l.append(arr[5])
        l.append(arr[3])
        l.append(arr[4])
    return l
def query_main_brief(time):
    cn_name = ''
    b_temp = ''
    b_desc = ''
    rst = dbsession.query(weather_detail.w_area,weather_detail.d_one).filter(weather_detail.w_time==time)
    for row in rst:
        print 'xxxxxxxxxxxxxxxx'
        cn_name += row[0]+','
        arr = row[1].split(',')
        b_temp += arr[3]+','
        print arr[2]
        b_desc += wdesc[arr[2]]+','
    cn_name = cn_name[:len(cn_name)-1]
    b_temp = b_temp[:len(b_temp)-1]
    b_desc = b_desc[:len(b_desc)-1]
    icon = b_desc.split(',')[0]
    temp = b_temp.split(',')[0]
    desc = cn_name.split(',')[0]

    return icon,desc,temp,b_temp,b_desc,cn_name
def allWeather(time):
    for city in city_cn:
        requestWeather(city,time)
def requestWeather(area,time):
    c = dbsession.query(weather_detail).filter(weather_detail.w_time==time,weather_detail.w_area==city_cn[area]).count()
    if c == 0:
        nmc = urllib.urlopen('http://www.nmc.cn/publish/forecast/'+area+'.html').read()

        d1 = getBrief(nmc,0)
        d2 = getBrief(nmc,d1[0])
        d3 = getBrief(nmc,d2[0])
        d4 = getBrief(nmc,d3[0])
        d5 = getBrief(nmc,d4[0])
        d6 = getBrief(nmc,d5[0])
        d7 = getBrief(nmc,d6[0])

        detail = getDetail(nmc)

        # i = t_weather.insert().values(w_time='20160526',w_area=u'昌平',d_one=unicode(d1[1]))
        # conn.execute(i)
        wd = weather_detail()
        wd.w_time = time
        wd.w_area = city_cn[area]
        wd.d_one = unicode(d1[1])
        wd.d_two = unicode(d2[1])
        wd.d_three = unicode(d3[1])
        wd.d_four = unicode(d4[1])
        wd.d_five = unicode(d5[1])
        wd.d_six = unicode(d6[1])
        wd.d_seven = unicode(d7[1])
        wd.w_detail = buffer(detail)
        dbsession.add(wd)
        dbsession.flush()
        dbsession.commit()

def getBrief(nmc,day):
    brief = ''

    s_day = 'dname">'
    today_index = nmc.find(s_day,day)
    wdesc_index_end = nmc.find('</p>',today_index+len(s_day))
    today = nmc[today_index+len(s_day):wdesc_index_end]
    len_day = len(today)+len(s_day)
    print today

    # today_week_index = nmc.find('week',today_index)
    today_week = nmc[today_index+len_day+11:today_index+len_day+11+9]
    if len(today_week.replace(' ','')) == 1:
        today_week_start = nmc.find('<td>',today_index+len_day+11+9)
        today_week_end = nmc.find('</td>',today_week_start)
        today_week = nmc[today_week_start+4:today_week_end]
    today_week = today_week.replace(' ','')
    print today_week


    s_wdesc = 'wdesc">'
    today_wdesc_index = nmc.find(s_wdesc,today_index)
    wdesc_index_end = nmc.find('</td> ',today_wdesc_index+len(s_wdesc))
    today_wdesc = nmc[today_wdesc_index+len(s_wdesc):wdesc_index_end]
    print today_wdesc

    s_temp = 'temp">'
    today_temp_index = nmc.find(s_temp,today_index)
    temp_index_end = nmc.find('</td> ',today_temp_index+len(s_temp))
    today_temp = nmc[today_temp_index+len(s_temp):temp_index_end]
    today_temp = today_temp.replace(' ','').replace(u'℃','')
    print today_temp

    s_direct = 'direct">'
    today_direct_index = nmc.find(s_direct,today_index)
    direct_index_end = nmc.find('</td> ',today_direct_index+len(s_direct))
    today_direct = nmc[today_direct_index+len(s_direct):direct_index_end]
    print today_direct

    s_power = 'power">'
    today_power_index = nmc.find(s_power,today_index)
    power_index_end = nmc.find('</td> ',today_power_index+len(s_power))
    today_power = nmc[today_power_index+len(s_power):power_index_end]
    print today_power
    print '\r\n.'

    brief = today+','+today_week+','+today_wdesc+','+today_temp+','+today_direct+','+today_power
    return power_index_end,brief

def getDetail(nmc):
    vars = locals()
    #时间
    time = ''
    vars['time_0_end'] = nmc.find('day0')
    for i in range(0, 8):
        j = i+1
        vars['time_'+str(j)+'_start'] = nmc.find('12px;">',vars['time_'+str(i)+'_end'])+16
        vars['time_'+str(j)+'_end'] = nmc.find('</div>',vars['time_'+str(j)+'_start'])-8
        vars['time'+str(j)] = nmc[vars['time_'+str(j)+'_start']:vars['time_'+str(j)+'_end']].replace(' ','')
        # print vars['time'+str(j)]
        time += vars['time'+str(j)]+','
    time = time[:len(time)-1]
    print time
    #
    #天气图标
    icon = ''
    vars['icon_0_end'] = nmc.find('h3_tqxx">')
    for i in range(0,8):
        j = i+1
        vars['icon_'+str(j)+'_start'] = nmc.find('<div>',vars['icon_'+str(i)+'_end'])+14
        vars['icon_'+str(j)+'_end'] = nmc.find('</div>',vars['icon_'+str(j)+'_start'])-8
        vars['icon'+str(j)] = nmc[vars['icon_'+str(j)+'_start']:vars['icon_'+str(j)+'_end']]
        vars['icon'+str(j)] = vars['icon'+str(j)].replace('/static','http://www.nmc.cn/static')
        # print vars['icon'+str(j)]
        icon += vars['icon'+str(j)]+','
    icon = icon[:len(icon)-1]
    print icon
    #
    #温度
    temp = ''
    vars['temp_0_end'] = nmc.find('h3_wd">')
    for i in range(0,8):
        j = i+1
        vars['temp_'+str(j)+'_start'] = nmc.find('<div>',vars['temp_'+str(i)+'_end'])+14
        vars['temp_'+str(j)+'_end'] = nmc.find('</div>',vars['temp_'+str(j)+'_start'])-9
        vars['temp'+str(j)] = nmc[vars['temp_'+str(j)+'_start']:vars['temp_'+str(j)+'_end']]
        vars['temp'+str(j)] = vars['temp'+str(j)]
        # print vars['temp'+str(j)]
        temp += vars['temp'+str(j)]+','
    temp = temp[:len(temp)-1]
    print temp
    #
    #降水
    js = ''
    vars['js_0_end'] = nmc.find('h3_js">')
    for i in range(0,8):
        j = i+1
        vars['js_'+str(j)+'_start'] = nmc.find('<div>',vars['js_'+str(i)+'_end'])+15
        vars['js_'+str(j)+'_end'] = nmc.find('</div>',vars['js_'+str(j)+'_start'])-9
        vars['js'+str(j)] = nmc[vars['js_'+str(j)+'_start']:vars['js_'+str(j)+'_end']]
        vars['js'+str(j)] = vars['js'+str(j)]
        # print vars['js'+str(j)]
        js += vars['js'+str(j)]+','
    js = js[:len(js)-1]
    print js
    #
    #风量
    fl = ''
    vars['fl_0_end'] = nmc.find('h3_fl">')
    for i in range(0,8):
        j = i+1
        vars['fl_'+str(j)+'_start'] = nmc.find('<div>',vars['fl_'+str(i)+'_end'])+14
        vars['fl_'+str(j)+'_end'] = nmc.find('</div>',vars['fl_'+str(j)+'_start'])-8
        vars['fl'+str(j)] = nmc[vars['fl_'+str(j)+'_start']:vars['fl_'+str(j)+'_end']]
        vars['fl'+str(j)] = vars['fl'+str(j)]
        # print vars['fl'+str(j)]
        fl += vars['fl'+str(j)]+','
    fl = fl[:len(fl)-1]
    print fl
    #
    #风向
    fx = ''
    vars['fx_0_end'] = nmc.find('h3_fx">')
    for i in range(0,8):
        j = i+1
        vars['fx_'+str(j)+'_start'] = nmc.find('<div>',vars['fx_'+str(i)+'_end'])+14
        vars['fx_'+str(j)+'_end'] = nmc.find('</div>',vars['fx_'+str(j)+'_start'])-8
        vars['fx'+str(j)] = nmc[vars['fx_'+str(j)+'_start']:vars['fx_'+str(j)+'_end']]
        vars['fx'+str(j)] = vars['fx'+str(j)]
        # print vars['fx'+str(j)]
        fx += vars['fx'+str(j)]+','
    fx = fx[:len(fx)-1]
    print fx
    #
    #气压
    qy = ''
    vars['qy_0_end'] = nmc.find('h3_qy">')
    for i in range(0,8):
        j = i+1
        vars['qy_'+str(j)+'_start'] = nmc.find('<div>',vars['qy_'+str(i)+'_end'])+14
        vars['qy_'+str(j)+'_end'] = nmc.find('</div>',vars['qy_'+str(j)+'_start'])-8
        vars['qy'+str(j)] = nmc[vars['qy_'+str(j)+'_start']:vars['qy_'+str(j)+'_end']]
        vars['qy'+str(j)] = vars['qy'+str(j)]
        # print vars['qy'+str(j)]
        qy += vars['qy'+str(j)]+','
    qy = qy[:len(qy)-1]
    print qy
    #
    #相对湿度
    xdsd = ''
    vars['xdsd_0_end'] = nmc.find('h3_xdsd">')
    for i in range(0,8):
        j = i+1
        vars['xdsd_'+str(j)+'_start'] = nmc.find('<div>',vars['xdsd_'+str(i)+'_end'])+14
        vars['xdsd_'+str(j)+'_end'] = nmc.find('</div>',vars['xdsd_'+str(j)+'_start'])-8
        vars['xdsd'+str(j)] = nmc[vars['xdsd_'+str(j)+'_start']:vars['xdsd_'+str(j)+'_end']]
        vars['xdsd'+str(j)] = vars['xdsd'+str(j)]
        # print vars['xdsd'+str(j)]
        xdsd += vars['xdsd'+str(j)]+','
    xdsd = xdsd[:len(xdsd)-1]
    print xdsd
    #
    #云量
    yl = ''
    vars['yl_0_end'] = nmc.find('h3_yl">')
    for i in range(0,8):
        j = i+1
        vars['yl_'+str(j)+'_start'] = nmc.find('<div>',vars['yl_'+str(i)+'_end'])+14
        vars['yl_'+str(j)+'_end'] = nmc.find('</div>',vars['yl_'+str(j)+'_start'])-8
        vars['yl'+str(j)] = nmc[vars['yl_'+str(j)+'_start']:vars['yl_'+str(j)+'_end']]
        vars['yl'+str(j)] = vars['yl'+str(j)]
        # print vars['yl'+str(j)]
        yl += vars['yl'+str(j)]+','
    yl = yl[:len(yl)-1]
    print yl
    #
    #能见度
    njd = ''
    vars['njd_0_end'] = nmc.find('h3_njd">')
    for i in range(0,8):
        j = i+1
        vars['njd_'+str(j)+'_start'] = nmc.find('<div>',vars['njd_'+str(i)+'_end'])+15
        vars['njd_'+str(j)+'_end'] = nmc.find('</div>',vars['njd_'+str(j)+'_start'])-8
        vars['njd'+str(j)] = nmc[vars['njd_'+str(j)+'_start']:vars['njd_'+str(j)+'_end']]
        vars['njd'+str(j)] = vars['njd'+str(j)]
        # print vars['njd'+str(j)]
        njd += vars['njd'+str(j)]+','
    njd = njd[:len(njd)-1]
    print njd
    #
    detail = time+'|'+icon+'|'+temp+'|'+js+'|'+fl+'|'+fx+'|'+qy+'|'+xdsd+'|'+yl+'|'+njd
    return detail
if __name__=='__main__':
    # r = requestWeather()
    # allWeather('20150625')
    # query_main_brief('20150625')
    query_chart(u'昌平')
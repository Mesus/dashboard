#coding:utf-8
import os,sys,xlrd
reload(sys)
sys.setdefaultencoding( "utf-8" )
def paser_xls(filename):
    # filename = sys.path[0]+'/'+filename
    data = xlrd.open_workbook(filename, 'rb')
    sheet_num =  len(data.sheets())
    print sheet_num
    s = []
    edge = []
    for i in range(0,sheet_num):
        sheet = data.sheet_by_index(i)
        for row in range(1,sheet.nrows):
            temp = []
            for col in range(sheet.ncols):
                cv = sheet.cell_value(row,col)
                if col == 0:
                    temp.append(cv)
                if col == 1:
                    temp.append(cv)
                if col == 2:
                    temp.append(cv)
                if col == 3:
                    temp.append(cv)
                if col == 4:
                    temp.append(cv)
                # if col == 5:
                #     temp.append(cv)
                # if col == 6:
                #     temp.append(cv)
                if col == 5 and len(cv)>0:
                    edge.append(cv)
            s.append(temp)
    return s,edge

def product(s):
    node = ''
    for row in s[0]:
        node += '{'
        for l in range(len(row)):
            if l == 0:
                node += 'id:'+str(row[l])+','
            if l == 1:
                node += "label:'"+str(row[l])+"',"
            if l == 2:
                node += "font:'"+str(row[l])+"',"
            if l == 3:
                node += 'group:'+str(row[l])+','
            if l == 4:
                node += 'value:'+str(row[l])+','
            # if l == 5:
            #     node += 'x:'+str(row[l])+','
            # if l == 6:
            #     node += 'y:'+str(row[l])
        node += '},\r\n'
    node = node[:len(node)-3]
    nodes = 'var nodes = [\r\n'+node+'];'

    edge = ''
    for r in s[1]:
        ft = str(r).split('-')
        edge += '{from:'+ft[0]+',to:'+ft[1]+'},\r\n'
    edge = edge[:len(edge)-3]
    edges = 'var edges = [\r\n'+edge+'];'

    return nodes+'\r\n'+edges
def wfile(fn,js):
    # fn = str(fn).replace('xls','js')
    fp = sys.path[0]+'/static/tts/'+fn+'.js'
    file_object = open(fp, 'w')
    file_object.write(js)
    file_object.close( )

if __name__=='__main__':
    sal = len(sys.argv)
    if sal > 1:
        fn = sys.argv[1]
        s = paser_xls(fn)
        js = product(s)
        j = sys.argv[2]
        wfile(j,js)
    else:
        print 'Parameter is not complete'
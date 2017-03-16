# encoding: utf-8
import xlrd,sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class CreateVis:
    def __init__(self):
        print ''
    def create(self,fn):
        filename = sys.path[0]+'/app/static/ds/'+ fn +'.xls'
        data = xlrd.open_workbook(filename, 'rb')

        scode = ''
        sheet = data.sheet_by_index(0)
        for row in range(1,sheet.nrows):
            node_tmp = "nodes.push("
            for col in range(sheet.ncols):
                ct = sheet.cell_type(row,col)
                val = sheet.cell_value(row,col)
                if col == 0:
                    node_tmp += '{id:' + str(val) +','
                if col == 1:
                    node_tmp += "label:'" + val + "',"
                if col == 2:
                    node_tmp += "group:'" + val + "',"
                if col == 3:
                    node_tmp += 'value:' + str(val) +'});'
            scode += node_tmp +'\r\n'

        sheet = data.sheet_by_index(1)
        for row in range(1,sheet.nrows):
            edge_tmp = "edges.push("
            for col in range(sheet.ncols):
                ct = sheet.cell_type(row,col)
                val = sheet.cell_value(row,col)
                if col == 0:
                    edge_tmp += '{from:' + str(val) +','
                if col == 1:
                    edge_tmp += "to:" + str(val) + ","
                if col == 2:
                    edge_tmp += "length:" + str(val) + ","
                if col == 3:
                    edge_tmp += 'width:' + str(val) +','
                if col == 4:
                    edge_tmp += "label:'" + val +"'});"
            scode += edge_tmp +'\r\n'
        print scode
        return scode
    def group(self,fn):
        filename = sys.path[0]+'/app/static/ds/'+ fn +'.xls'
        data = xlrd.open_workbook(filename, 'rb')

        g_list = []
        sheet = data.sheet_by_index(2)
        for row in range(sheet.nrows):
            for col in range(1,sheet.ncols):
                val = sheet.cell_value(row,col)
                g_list.append(val)
        return g_list
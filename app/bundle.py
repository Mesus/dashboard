# encoding: utf-8
import sys,json
reload(sys)
sys.setdefaultencoding( "utf-8" )
class CCode:
    def str(self, content, encoding='utf-8'):
        # 只支持json格式
        # indent 表示缩进空格数
        return json.dumps(content, encoding=encoding, ensure_ascii=False, indent=4)
        pass

    pass
def tojson(csv):
    data = []
    size = 1
    for line in open(csv,'r').readlines():
        l_arr = line.split(',')
        d = {}
        # print unicode(str(l_arr[0]),'utf-8')
        d['name'] = str(l_arr[0]).encode('utf-8')

        d['size'] = size
        size += 1
        tmp = []
        for i in range(1,len(l_arr)):
            im = str(l_arr[i]).replace('\n','').encode('utf-8')
            if len(im) > 0:
                tmp.append(im)
                d['imports'] = tmp
        data.append(d)

    # print data
    # json = demjson.encode(data)
    # print json
    # text = demjson.decode(json)
    # print text
    cCode = CCode()
    t = cCode.str(data)
    # print t
    with open(sys.path[0]+'/static/tts/data.json', 'w') as outfile:
        # simplejson.dump(data,outfile)
        outfile.write(t)
        outfile.close()

if __name__=='__main__':
    sal = len(sys.argv)
    if sal > 0:
        fn = sys.argv[1]
        tojson(fn)
        print '生成文件:'+sys.path[0]+'/static/tts/data.json'
    else:
        print 'Parameter is not complete'


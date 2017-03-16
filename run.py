# -*- coding: utf-8 -*-

from app import app

if __name__ == '__main__':

    # context = ('vssl.crt', 'vssl.key')

    app.debug=True # 设置调试模式，生产模式的时候要关掉debug

    # app.run(host='0.0.0.0',port=9000,ssl_context=context) # 启动服务器
    app.run(host='0.0.0.0',port=9999)
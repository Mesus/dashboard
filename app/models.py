#coding:utf8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,mapper

sqlite_engine = create_engine('sqlite:///dashboard.db', echo=True)


metadata = MetaData()

t_product = Table(
    "product",metadata,
    Column('t_id', Integer, primary_key=True),
    Column('area',VARCHAR(255), nullable=True),
    Column('pmdm',VARCHAR(255), nullable=True),
    Column('pm', VARCHAR(255), nullable=True),
    Column('pl', VARCHAR(255), nullable=True),
    Column('csl',Numeric(255,3),nullable=True),
    Column('ckl',Numeric(255,3),nullable=True),
    Column('jpckc',Numeric(255,3),nullable=True),
    Column('spckc',Numeric(255,3),nullable=True),
    Column('yjccl',Numeric(255,3),nullable=True),
    Column('data_time', VARCHAR(255), nullable=True),
    Column('t_time',TIMESTAMP,nullable=False,server_default = func.now())
)

t_sell = Table(
    "sell",metadata,
    Column('s_id', Integer, primary_key=True),
    Column('xsl',Numeric(255,3),nullable=True),
    Column('kgl',Numeric(255,3),nullable=True),
    Column('dbl',Numeric(255,3),nullable=True),
    Column('data_time', VARCHAR(255), nullable=True),
    Column('t_time',TIMESTAMP,nullable=False,server_default = func.now())
)

t_logis = Table(
    "logistics",metadata,
    Column('t_id', Integer, primary_key=True),
    Column('cc',Integer,nullable=True),
    Column('ccl',Integer,nullable=True),
    Column('cql',Integer,nullable=True),
    Column('data_time', VARCHAR(255), nullable=True),
    Column('t_time',TIMESTAMP,nullable=False,server_default = func.now()),
    Column('gk_wd',Numeric(255,2),nullable=True),
    Column('gk_dp',Numeric(255,2),nullable=True)
)

t_loss_inventory = Table(
    "loss_inventory",metadata,
    Column('tid', INTEGER, primary_key=True),
    Column('farm',VARCHAR(255), nullable=True),
    Column('s_time', VARCHAR(255), nullable=True),
    Column('e_time', VARCHAR(255), nullable=True),
    Column('insert_time',VARCHAR(255),nullable=True),
    Column('number',NUMERIC(255,3),nullable=True),
    Column('number_1',NUMERIC(255,3),nullable=True),
    Column('ratio',NUMERIC(255,3),nullable=True),
    Column('pm',VARCHAR(255),nullable=True),
    Column('type',INTEGER,nullable=True),
    Column('t_user',VARCHAR(255),nullable=True),
    Column('t_time',TIMESTAMP,nullable=False,server_default = func.now())
)

t_loss_process = Table(
    "loss_process",metadata,
    Column('tid', INTEGER, primary_key=True),
    Column('farm',VARCHAR(255), nullable=True),
    Column('s_time', VARCHAR(255), nullable=True),
    Column('e_time', VARCHAR(255), nullable=True),
    Column('insert_time',VARCHAR(255),nullable=True),
    Column('number',NUMERIC(255,3),nullable=True),
    Column('number_1',NUMERIC(255,3),nullable=True),
    Column('ratio',NUMERIC(255,3),nullable=True),
    Column('pm',VARCHAR(255),nullable=True),
    Column('type',INTEGER,nullable=True),
    Column('t_user',VARCHAR(255),nullable=True),
    Column('t_time',TIMESTAMP,nullable=False,server_default = func.now())
)

t_loss_allot = Table(
    "loss_allot",metadata,
    Column('tid', INTEGER, primary_key=True),
    Column('s_farm',VARCHAR(255), nullable=True),
    Column('d_farm',VARCHAR(255), nullable=True),
    Column('s_time', VARCHAR(255), nullable=True),
    Column('d_time', VARCHAR(255), nullable=True),
    Column('insert_time',VARCHAR(255),nullable=True),
    Column('number',NUMERIC(255,3),nullable=True),
    Column('number_1',NUMERIC(255,3),nullable=True),
    Column('ratio',NUMERIC(255,3),nullable=True),
    Column('pm',VARCHAR(255),nullable=True),
    Column('type',INTEGER,nullable=True),
    Column('t_user',VARCHAR(255),nullable=True),
    Column('t_time',TIMESTAMP,nullable=False,server_default = func.now())
)

t_pm = Table(
    "pm",metadata,
    Column('pmdm', VARCHAR(255), primary_key=True),
    Column('pmmc',VARCHAR(255), nullable=False)
)

t_weather = Table(
    "weather_detail",metadata,
    Column('wid', INTEGER, primary_key=True),
    Column('w_time',VARCHAR(10),nullable=True),
    Column('w_area',VARCHAR(50),nullable=True),
    Column('d_one',VARCHAR(255),nullable=True),
    Column('d_two',VARCHAR(255),nullable=True),
    Column('d_three',VARCHAR(255),nullable=True),
    Column('d_four',VARCHAR(255),nullable=True),
    Column('d_five',VARCHAR(255),nullable=True),
    Column('d_six',VARCHAR(255),nullable=True),
    Column('d_seven',VARCHAR(255),nullable=True),
    Column('w_detail',BLOB,nullable=True),
    Column('sys_time',TIMESTAMP,nullable=False,server_default = func.now())
)
class product(object):
    # 表的名字:
    __tablename__ = 'product'
    # 表的结构:
    tid = Column(Integer,primary_key=True)  #
    area = Column(String(255))
    pmdm = Column(String(255))
    pm = Column(String(255))
    pl = Column(String(255))
    csl = Column(DECIMAL())
    ckl = Column(DECIMAL())
    jpckc = Column(DECIMAL())
    spckc = Column(DECIMAL())
    yjccl = Column(DECIMAL())
    data_time = Column(String(255))

class sell_t(object):
    # 表的名字:
    __tablename__ = 'sell'
    # 表的结构:
    sid = Column(Integer,primary_key=True)  #
    xsl = Column(DECIMAL())
    kgl = Column(DECIMAL())
    dbl = Column(DECIMAL())
    data_time = Column(String(255))

class logistics(object):
    # 表的名字:
    __tablename__ = 'logistics'
    # 表的结构:
    tid = Column(Integer,primary_key=True)  #
    cc = Column(Integer)
    ccl = Column(Integer)
    cql = Column(Integer)
    data_time = Column(String(255))
    gk_wd = Column(DECIMAL())
    gk_dp = Column(DECIMAL())

class li(object):
    # 表的名字:
    __tablename__ = 'loss_inventory'
    # 表的结构:
    tid = Column(Integer,primary_key=True)  #
    farm = Column(String(255))
    number = Column(DECIMAL())
    number_1 = Column(DECIMAL())
    ratio = Column(DECIMAL())
    s_time = Column(String(255))
    e_time = Column(String(255))
    insert_time = Column(String(255))
    type = Column(Integer)
    pm = Column(String(255))

class lp(object):
    # 表的名字:
    __tablename__ = 'loss_process'
    # 表的结构:
    tid = Column(Integer,primary_key=True)  #
    farm = Column(String(255))
    number = Column(DECIMAL())
    number_1 = Column(DECIMAL())
    ratio = Column(DECIMAL())
    s_time = Column(String(255))
    e_time = Column(String(255))
    insert_time = Column(String(255))
    type = Column(Integer)
    pm = Column(String(255))

class la(object):
    # 表的名字:
    __tablename__ = 'loss_allot'
    # 表的结构:
    tid = Column(Integer,primary_key=True)  #
    s_farm = Column(String(255))
    d_farm = Column(String(255))
    number = Column(DECIMAL())
    number_1 = Column(DECIMAL())
    ratio = Column(DECIMAL())
    user = Column(String(255))
    s_time = Column(String(255))
    d_time = Column(String(255))
    type = Column(Integer)
    pm = Column(String(255))
    insert_time = Column(String(255))

class pm(object):
    __tablename__ = 'pm'
    # 表的结构:
    pmdm = Column(String(255),primary_key=True)  #
    pmmc = Column(String(255))

class weather_detail(object):
    __tablename__ = 'weather_detail'
    wid = Column(Integer,primary_key=True)
    w_time = Column(String(10))
    w_area = Column(String(50))
    d_one = Column(String(255))
    d_two = Column(String(255))
    d_three = Column(String(255))
    d_four = Column(String(255))
    d_five = Column(String(255))
    d_six = Column(String(255))
    d_seven = Column(String(255))
    w_detail = Column(BLOB)

metadata.create_all(sqlite_engine)

mapper(product, t_product)
mapper(li, t_loss_inventory)
mapper(lp, t_loss_process)
mapper(la, t_loss_allot)
mapper(pm,t_pm)
mapper(weather_detail,t_weather)
mapper(sell_t,t_sell)
mapper(logistics,t_logis)

DBSession = sessionmaker(bind=sqlite_engine)
dbsession = DBSession()
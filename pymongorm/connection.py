# coding=utf-8
"""
说明: 底层数据库连接
作者:pengxin.wu 15645060726@163.com
创建时间: 2017-04-11 11:32:51
"""
from pymongo import MongoClient
from exception import MongoConectErr

mongo_configure = None


class MongoDB(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if MongoDB._instance:
            return MongoDB._instance
        else:
            MongoDB._instance = super(MongoDB, cls).__new__(cls, *args)
            return MongoDB._instance

    def __init__(self):
        """
        创建mongo客户端连接池
        :return:
        """
        global mongo_configure
        if mongo_configure is None:
            raise BaseException("mongo未进行配置")

        self.pool_size = mongo_configure.pool_size
        self.host = mongo_configure.host
        self.port = mongo_configure.port
        self.timeout = mongo_configure.timeout
        self.client = MongoClient(host=self.host, port=self.port, maxPoolSize=self.pool_size,
                                  connectTimeoutMS=1000*self.timeout)
        MongoDB._instance = self

    def get_connect(self, db, collect):
        """
        :return:
        """
        return self.client[db][collect]


class Config(object):
    def __init__(self, ip, port, user, password, pool_size, timeout):
        user_passwd = None
        if user:
            user_passwd = user
        if password:
            user_passwd = "%s:%s" % (user_passwd, password)
        if user_passwd:
            self.host = "mongodb://%s@%s" % (user_passwd, ip)
        else:
            self.host = ip

        self.pool_size = pool_size
        self.port = port
        self.timeout = timeout


def set_configure(ip="localhost", port=27017, user=None, password=None, pool_size=10, timeout=30):
    global mongo_configure
    mongo_configure = Config(ip, port, user, password, pool_size, timeout)

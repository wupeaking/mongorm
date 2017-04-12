# coding=utf-8
"""
说明: 定义自己的异常类型
作者:pengxin.wu 15645060726@163.com
创建时间: 2017-04-11 11:55:57
"""


class MongormException(Exception):
    """
    mongoorm的基本异常
    """
    def __str__(self):
        return "产生了一些异常"


class MongoConectErr(MongormException):
    def __init__(self, info=None):
        self.info = info

    def __str__(self):
        return "连接数据库出现错误 %s " % self.info
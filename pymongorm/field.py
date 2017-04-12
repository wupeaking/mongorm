# coding=utf-8
"""
说明:定义mongo的字段类型
作者:pengxin.wu 15645060726@163.com
创建时间: 2017-04-11 10:27:23
"""
import bson


class AbstractField(object):
    """
    字段的抽象类 所有的字段属性
    mongo作为一个Nosql 对json是完全兼容的 所以至少json的所有字段类它应该是支持的
    """
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", str(self.__class__))
        self.args = args
        self.is_must = kwargs.get("is_must", False)
        if "default" in kwargs:
            self.default = kwargs["kwargs"]

    def convert_to_db(self, v):
        raise AttributeError("%s must overwrite the function" % self.name)


class IntField(AbstractField):
    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", 0)
        super(IntField, self).__init__(args, kwargs)

    def convert_to_db(self, v):
        value = int(v)
        if value < -2147483648 or value > 2147483647:
            raise ValueError("IntField is 32bit -2147483648 ~ 2147483647")
        else:
            return value


class LongField(AbstractField):
    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", None)
        super(LongField, self).__init__(args, kwargs)

    def convert_to_db(self, v):
        value = long(v)
        if value < -9223372036854775808 or value > 9223372036854775807:
            raise ValueError("longField is 64bit -9223372036854775808 ~ 9223372036854775807")
        else:
            return value


class FloatField(AbstractField):
    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", 0.00)
        super(FloatField, self).__init__(args, kwargs)

    def convert_to_db(self, v):
        try:
            value = float(v)
        except ValueError:
            raise ValueError("%s must float type", self.name)
        else:
            return value


class NumberFiled(AbstractField):
    """
    number字段包含int long float
    """
    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", 0)
        super(NumberFiled, self).__init__(args, kwargs)

    def convert_to_db(self, v):
        if isinstance(v, (float, int, long)):
            return v


class CharField(AbstractField):
    # mongo默认一个文档的最大长度不要超过16M
    _MAX_LENGTH = 16*1024*1024

    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", "")
        super(CharField, self).__init__(args, kwargs)
        self.max_length = kwargs.get("max_length", CharField._MAX_LENGTH)

    def convert_to_db(self, v):
        if isinstance(v, (unicode, str)):
            if len(v) > self.max_length:
                raise ValueError("CharField  max length is setted %s" % self.max_length)
            else:
                return v
        try:
            value = unicode(v)
        except ValueError:
            raise ValueError("%s must char type", self.name)
        else:
            return value


class DictField(AbstractField):
    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", {})
        super(DictField, self).__init__(args, kwargs)

    def convert_to_db(self, v):
        if isinstance(v, dict):
            return v
        else:
            raise ValueError("%s must dict type", self.name)


class ListField(AbstractField):
    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", [])
        super(ListField, self).__init__(args, kwargs)

    def convert_to_db(self, v):
        if isinstance(v, list):
            return v
        else:
            raise ValueError("%s must list type", self.name)


class NULLField(AbstractField):
    def __init__(self, *args, **kwargs):
        # self.default = kwargs.get("default", None)
        super(NULLField, self).__init__(args, kwargs)

    def convert_to_db(self, v):
        if isinstance(v, None):
            return v
        else:
            raise ValueError("%s must None type", self.name)


class ReferenceField(AbstractField):
    def __init__(self, refer_model):
        self.ref_cls = refer_model
        super(ReferenceField, self).__init__(is_must=True)

    def convert_to_db(self, v):
        assert isinstance(v, bson.ObjectId)
        return v



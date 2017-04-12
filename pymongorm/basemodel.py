# coding=utf-8
"""
说明: mongo的集合基类模型
作者:pengxin.wu 15645060726@163.com
创建时间: 2017-04-11 09:58:59
"""
from field import AbstractField
from field import ReferenceField
# from exception import MongormException
from connection import MongoDB
from bson import ObjectId


class MongoModelMange(object):
    def __init__(self, cls):
        self.model_cls = cls
        # 获取模型的所有字段名
        self.fields_name = getattr(self.model_cls, "__fields_name")

    @property
    def connection(self):
        dbname = self.model_cls.Meta.dbname
        collection = self.model_cls.Meta.collection
        return MongoDB().get_connect(dbname, collection)

    def create(self, **kwargs):
        """
        插入一条记录 返回创建的对象
        :param kwargs:
        :return:
        """
        # 验证所给的参数 是否在模型中定义
        self._auth_args_in_fields(kwargs.keys())
        # 创建mongo对象
        mongo_obj = dict()

        # 转换所有字段的为实际值 而不再是一个Field对象
        for attr in self.fields_name:
            attr_obj = getattr(self.model_cls, attr)
            # 检查是否是引用字段
            if isinstance(attr_obj, ReferenceField) and kwargs.get(attr, False):
                ref_id = self._process_reference(kwargs[attr])
                mongo_obj[attr] = ref_id
                continue

            # 检查这个字段是否是必须的
            if attr_obj.is_must:
                if attr not in kwargs.keys() and not hasattr(attr_obj, "default"):
                    raise ValueError("%s is a must attrbute" % attr)
                else:
                    mongo_obj[attr] = attr_obj.convert_to_db(
                            kwargs.get(attr, None) or getattr(attr_obj, "default", None))
            else:
                if attr in kwargs:
                    mongo_obj[attr] = attr_obj.convert_to_db(kwargs[attr])

        connect = self.connection
        return connect.insert_one(mongo_obj)

    def find(self, *args, **kwargs):
        # todo:: 暂时调用pymongo的原生接口
        cursor = self.connection.find(*args, **kwargs)
        # 总共查询到的个数
        total = cursor.count()
        while total > 0:
            total -= 1
            content = next(cursor)
            yield self.conent_object(content)
        raise StopIteration

    def find_one(self, filt, *args, **kwargs):
        content = self.connection.find_one(filter=filt, *args, **kwargs)
        return self.conent_object(content)

    def delete_one(self, filt):
        return self.connection.delete_one(filt)

    def delete_many(self, filt):
        self.connection.save()
        return self.delete_many(filt)

    def conent_object(self, content):
        """
        将返回的内容转换成对象
        :param content:
        :return:
        """
        assert isinstance(content, dict)
        model_obj = self.model_cls()
        for key in content.keys():
            # 查看此key是否是model_cls设置的
            attr_obj = getattr(self.model_cls, key, None)
            if isinstance(attr_obj, ReferenceField):
                ref_cls = attr_obj.ref_cls
                obj = ref_cls.objects.find_one({"_id": content[key]})
                setattr(model_obj, key, obj)
                continue
            setattr(model_obj, key, content[key])
        return model_obj

    @staticmethod
    def _process_reference(value):
        """
        处理引用字段
        :return:
        """
        if isinstance(value, ObjectId):
            return value

        if hasattr(value, "_id"):
            return getattr(value, "_id")
        else:
            insert = value.create()
            return insert.inserted_id

    def _auth_args_in_fields(self, keys):
        """
        验证所传递的参数是当前模型的所有字段名
        """
        for key in keys:
            if key not in self.fields_name:
                raise AttributeError("%s has no the %s attribute" % self.model_cls.__name__, key)


class MongoType(type):
    """
    继承type 增加元类的一些特别功能
    """
    # 定义一些保留属性名 这些属性名称不能用于mongo字段的定义
    _save_fields = {"create", "delete", "find", "find_one"}

    def __init__(cls, name, base, attr):
        super(MongoType, cls).__init__(name, base, attr)
        __fields_name, __fields_obj = MongoType._get_field_attr(cls)
        res = set(__fields_name) & MongoType._save_fields
        if res:
            raise AttributeError("%s 使用了保留的字段 %s" % (cls, res))

        setattr(cls, "__fields_name", __fields_name)
        objects = MongoModelMange(cls)
        setattr(cls, "objects", objects)

    @staticmethod
    def _get_field_attr(cls):
        """
        获取指定类下的字段对象的名称和实例
        :param cls:
        :return:
        """
        field_attr_obj = []
        field_attr_name = []
        for attr in dir(cls):
            attr_obj = getattr(cls, attr)
            if isinstance(attr_obj, AbstractField):
                field_attr_obj.append(attr_obj)
                field_attr_name.append(attr)
        return field_attr_name, field_attr_obj


class MongoModel(object):
    """
    mongo的orm的基类 该类重新定向了元类为MongoType 类也是一个对象 元类就是创建该类对象的父类
    一个model类被创建完成后 应当立刻具有一些功能 比如create delete find等功能
    """
    # 重新指明类的元类为MonType 类
    __metaclass__ = MongoType

    class Meta:
        dbname = "mongorm"
        collection = "test"

    def __init__(self, **kwargs):
        self.kw = kwargs

    # def __setattr__(self, key, value):
    #     if key == "create":
    #         raise MongormException("create是保留字段")
    #     else:
    #         self.__dict__[key] = value

    def __getattr__(self, item):
        if item == "create":
            def _create():
                return self.__class__.objects.create(**self.kw)
            return _create
        if item == "find_one":
            def _find_one(filt, *args, **kwargs):
                return self.__class__.objects.find_one(filter=filt, *args, **kwargs)
            return _find_one
        if item == "find":
            def _find(*args, **kwargs):
                return self.__class__.objects.find(*args, **kwargs)
            return _find
        else:
            return self.__dict__[item]

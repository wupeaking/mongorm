# coding=utf-8
"""
说明: 使用示例
作者:pengxin.wu 15645060726@163.com
创建时间: 2017-04-12 15:16:48
"""
from pymongorm import MongoModel
from pymongorm import CharField, IntField, ReferenceField

if __name__ == "__main__":
    class User(MongoModel):

        class Meta:
            dbname = "mongoorm"
            collection = "test"
        user = CharField(is_must=True)
        age = IntField(is_must=True)

    class Post(MongoModel):

        class Meta:
            dbname = "mongoorm"
            collection = "posts"  # 集合名词不能使用- 等特殊字符 可能是有问题
        author = ReferenceField(User)  # 引用字段 保存的是objectid
        title = CharField(is_must=True)
        count = IntField(default=0, is_must=True)

    from pymongorm.connection import set_configure
    set_configure("192.168.99.105", 27017, pool_size=10)
    # 下面两种方法均可以插入文档

    # User.objects.create(user="wupengxin", age=10)
    # print User(user="usertest", age=12).create()

    # 创建几个Post
    # for i in xrange(200):
    #     print Post(title="post title" + str(i), author=User(user="wupengxin" + str(i), age=i )).create()
    ret = Post.objects.find({"title": "post title0"})
    for r in ret:
        print r.author.user

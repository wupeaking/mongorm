## pymongorm
一个简单的基于pymongo的orm

### 使用示例

> 安装
```shell
1. 直接克隆github进行安装
# git clone git@github.com:wupeaking/mongorm.git
# cd mongorm
# python setup install

2. 使用pip安装
# pip install pymongorm # mongorm包名已经被使用了所有我换成了pymongorm

```

### 创建记录
```python
from pymongorm import MongoModel
from pymongorm import CharField, IntField
class User(MongoModel):

    class Meta:
        # 设置mongo的数据库名称
        dbname = "mongoorm"
        # 设置集合名词
        collection = "test"
    user = CharField(is_must=True, default="xxx")
    age = IntField(is_must=True)

if __name__ == "__main__":
    from pymongorm.connection import set_configure
    set_configure("localhost", 27017, pool_size=10)
    # 下面两种方法均可以插入一条记录
    User.objects.create(user="wupengxin", age=10)
    print User(user="usertest", age=12).create()

```

#### 创建有引用关系的记录
```python
from pymongorm import MongoModel
from pymongorm import CharField, IntField, ReferenceField
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

    # 创建几个Post
    for i in xrange(200):
        print Post(title="post title" + str(i), author=User(user="wupengxin" + str(i), age=i )).create()
```


#### 查找

```python
res = Post.objects.find({"title": "post title0"})
for r in res:
    print r.author.user
```

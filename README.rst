### mongorm
一个简单的基于pymongo的orm

### 使用示例


```python
from mongorm import MongoModel
from field import CharField, IntField
class User(MongoModel):

    class Meta:
        # 设置mongo的数据库名称
        dbname = "mongoorm"
        # 设置集合名词
        collection = "test"
    user = CharField(is_must=True, default="xxx")
    age = IntField(is_must=True)

if __name__ == "__main__":
    # 下面两种方法均可以插入一条记录
    User.objects.create(user="wupengxin", age=10)
    print User(user="usertest", age=12).create()
```

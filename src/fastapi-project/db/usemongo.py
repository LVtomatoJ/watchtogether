from pymongo import MongoClient
from ..models import User,Power


client = MongoClient('localhost', 27017)
db = client['whatchtogether']



def init():
    # 初始化
    pass

# user操作


def add_user(user:User):
    #如何level不存在返回None
    level = user.level
    if not get_power_by_level(level):
        return None
    # 添加一个user
    userdb = db['user']
    user_data = user.dict()
    result = userdb.insert_one(user_data)
    return result

def get_user_by_username(username:str):
    userdb = db['user']
    result = userdb.find_one({'username':username})
    try:
        return User(**result)
    except TypeError:
        return None
# power操作

def add_power(power: Power):
    # 添加一个等级
    powerdb = db['power']
    power_data = power.dict()
    result = powerdb.insert_one(power_data)
    return result.inserted_id


def get_power_by_level(level: int):
    # 获取一个等级
    powerdb = db['power']
    result = powerdb.find_one({'level': level})
    # 使用pydantic返回数据 如果为空返回none
    try:
        return Power(**result)
    except TypeError:
        return None


if __name__ == '__main__':
    # 添加0level最大5人非admin
    # print(add_power(Power(level=1,live_max_people_num=10,is_admin=0)))
    # 设置level位power中唯一索引
    # powerdb = db['power']
    # powerdb.create_index('level',unique=True)
    # print(get_power(3))
    # print(User(username="张三丰",password="613613",phone_number='15389064060',level=4,livetime=5))
    # print(get_user_by_username('张三丰'))
    # 设置phone为user中唯一索引
    # userdb = db['userdb']
    # userdb.create_index('phone_number',unique=True)
    pass

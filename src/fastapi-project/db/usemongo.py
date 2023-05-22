from pymongo import MongoClient
from ..models import User,Power,Live
from pydantic import parse_obj_as
from bson import ObjectId

client = MongoClient('localhost', 27017)
db = client['whatchtogether']



def init():
    # 初始化
    pass

# user操作

def add_user(user:User):
    #如果level不存在返回None
    level = user.level
    if not get_power_by_level(level):
        return None
    # 添加一个user
    userdb = db['user']
    user_data = user.dict()
    result = userdb.insert_one(user_data)
    return result.inserted_id

def update_user(user:User):
    #如果level不存在返回None
    level = user.level
    if not get_power_by_level(level):
        return None
    # 添加一个user
    userdb = db['user']
    user_data = user.dict()
    user_id = user_data.pop('id')
    print(user_id)
    print(user_data)
    result = userdb.replace_one({'_id':ObjectId(user_id)},user_data)
    return result.acknowledged


def get_user_by_username(username:str):
    userdb = db['user']
    result = userdb.find_one({'username':username})
    try:
        return User(**result,id=str(result['_id']))
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
    

#live

def add_live(live:Live):
    livedb = db['live']
    live_data = live.dict()
    result = livedb.insert_one(live_data)
    return result.inserted_id

if __name__ == '__main__':
    # 添加0level最大5人非admin
    # print(add_power(Power(level=1,live_max_people_num=10,is_admin=0)))
    # 设置level位power中唯一索引
    # powerdb = db['power']
    # powerdb.create_index('level',unique=True)
    # print(get_power(3))
    # print(User(username="张三丰",password="613613",phone_number='15389064060',level=4,livetime=5,is_admin=1))
    # print(get_user_by_username('张三丰'))
    # 设置phone为user中唯一索引
    # userdb = db['userdb']
    # userdb.create_index('phone_number',unique=True)
    # get_user_by_username('张三丰')
    pass


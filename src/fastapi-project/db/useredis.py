import redis
import time

# 连接Redis服务器
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def create_live(live_id:str):

    redis_client.zadd()

def add_online_user(live_id:str,user_id:str):
    # 将用户添加到在线用户列表中
    timestamp = int(time.time())  # 获取当前时间戳
    online_users_key = f'live_room:{live_id}:online_users'
    redis_client.zadd(online_users_key, {user_id: timestamp})

def remove_online_user(live_id,user_id):
    # 将用户从在线用户列表中移除
    online_users_key = f'live_room:{live_id}:online_users'
    redis_client.zrem(online_users_key, user_id)

def get_online_users(live_id:str,limit=10):
    # 获取在线用户列表
    online_users_key = f'live_room:{live_id}:online_users'
    online_users = redis_client.zrevrangebyscore(online_users_key, '+inf', '-inf',
                                                 start=0, num=limit, withscores=True)
    # 将元组转换为字典，方便后续处理
    online_users_dict = dict(online_users)

    return online_users_dict

# 测试代码
if __name__ == '__main__':
    pass
    # # 添加用户1和用户2到在线用户列表
    # add_online_user('user1')
    # add_online_user('user2')

    # # 获取前3个在线用户
    # online_users = get_online_users(limit=3)
    # print('Online users:', online_users)  # 输出：{'user2': timestamp2, 'user1': timestamp1}

    # # 移除用户1
    # remove_online_user('user1')

    # # 获取前2个在线用户
    # online_users = get_online_users(limit=2)
    # print('Online users:', online_users)  # 输出：{'user2': timestamp2}
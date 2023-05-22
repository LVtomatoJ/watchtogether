from fastapi import APIRouter,Depends,HTTPException,status
from ..dependencies import check_token_user
from ..models import OutUser,User,Power,InLive,Live
from ..db.usemongo import get_power_by_level,add_live,update_user
import datetime
import hashlib
from ..config import LIVE_KEY,LIVE_PUSH_DOMAIN


def make_push_url(endtime,live_id):
    md5 = hashlib.md5()
    end_time_stamp = end_time.timestamp()
    txTime = hex(int(end_time_stamp))[2:].upper()
    #拼接推流地址
    text = LIVE_KEY+'live_id'+ txTime
    md5.update(text.encode('utf-8'))
    txSecret = md5.hexdigest()
    push_url = r"rtmp://{}/live/{}?txSecret={}&txTime={}".format(LIVE_PUSH_DOMAIN,live_id,txSecret,txTime)
    return push_url

router = APIRouter(prefix='/live')

@router.post('/create')
async def create_live(inlive:InLive,user:User = Depends(check_token_user)):
    #获取等级内容
    level = user.level
    power:Power = get_power_by_level(level=level)
    live_max_people_num = power.live_max_people_num
    #判断人数是否超出
    if live_max_people_num<=inlive.max_people:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="人数超出当前等级最大人数")
    #判断剩余时间是否足够
    if user.livetime<inlive.times:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="时间超出当前剩余最大时间")
    leave_time = user.livetime-inlive.times#剩余时间
    
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=inlive.times)
    end_time = now + delta#结束时间
    #添加到数据库
    live = Live(**inlive.dict(),user_id=user.id,endtime=end_time,status=0)
    live_id = add_live(live=live)
    if not live_id:
        #添加到mongo失败
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="添加数据库失败")
    #扣除剩余时间
    user.livetime = leave_time
    result = update_user(user=user)
    if not result:
        #更新剩余时间错误
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="更新剩余时间错误")
    #获取推流地址
    push_url = make_push_url(endtime=end_time,live_id=live_id)
    return push_url
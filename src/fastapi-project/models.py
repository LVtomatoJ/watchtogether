from typing import Union
from pydantic import BaseModel, Field, conint, validator
from bson import ObjectId
from datetime import datetime
from typing import Optional
import re


class Power(BaseModel):
    level: conint(ge=0, le=99)  # 这里使用coint限制level的值只能是int类型0-99
    live_max_people_num: conint(ge=0, le=99)

class OutUser(BaseModel):
    id:str
    username: str
    phone_number: str
    level: conint(ge=0, le=99)  # 这里使用coint限制level的值只能是int类型0-99
    livetime: conint(ge=0, le=9999)  # 这里使用coint限制level的值只能是int类型0-9999
    is_admin:conint(ge=0,le=1) #是否admin 0-1
    class Config:
        arbitrary_types_allowed = True
    # 用户名长度校验
    @validator('username')
    def check_username_length(cls, v):
        if len(v) < 3 or len(v) > 10:
            raise ValueError('用户名长度为2-10位')
        return v

    # 用户名内容校验
    @validator('username')
    def check_username_characters(cls, v):
        pattern = r'^[\u4e00-\u9fa5a-z0-9_]+$'
        if not re.match(pattern, v):
            raise ValueError('用户名只能包含中文字符小写字母数字和下划线')
        return v

    # 手机号长度校验
    @validator('phone_number')
    def check_phone_number(cls, v):
        pattern = r'^1\d{10}$'
        if not re.match(pattern, v):
            raise ValueError('手机号格式错误')
        return v

class User(OutUser):
    password: str


#token

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    username: str
    guest:int

#live

class InLive(BaseModel):
    title:str
    max_people:conint(ge=0, le=99)
    times:conint(ge=0, le=99)
    is_public:conint(ge=0,le=1)
    password:str

    # 标题长度校验
    @validator('title')
    def check_title_length(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('标题长度为3-20位')
        return v
    
class Live(InLive):
    id:Optional[str] = None
    user_id:str
    status:conint(ge=0,le=2)
    endtime:datetime
    times:Optional[int] = None



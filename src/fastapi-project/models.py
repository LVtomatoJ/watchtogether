from typing import Union
from pydantic import BaseModel, conint, validator
import re

class Power(BaseModel):
    level: conint(ge=0, le=99)  # 这里使用coint限制level的值只能是int类型0-99
    live_max_people_num: int
    is_admin: conint(ge=0, le=1)  # 这里使用coint限制is_admin的值只能是int类型0或1


class User(BaseModel):
    username: str
    password: str
    phone_number: str
    level: conint(ge=0, le=99)  # 这里使用coint限制level的值只能是int类型0-99
    livetime: conint(ge=0, le=9999)  # 这里使用coint限制level的值只能是int类型0-9999

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


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    username: str
    guest:int
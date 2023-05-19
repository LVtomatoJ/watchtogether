import random
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..db import usemongo as db
from ..models import Token
from ..config import SECRET_KEY,ALGORITHM,ACCESS_USER_TOKEN_EXPIRE_MINUTES,ACCESS_GUEST_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from jose import JWTError, jwt


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter()


@router.post('/token', response_model=Token)
async def get_token_by_username(form_data:OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username=='guest':
        #返回匿名用户token
        username = 'guest'+str(random.randint(1000,10000)) 
        access_token_expires = timedelta(minutes=ACCESS_GUEST_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={'sub':username,'guest':1},expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer","username":username}
    else:
        #返回注册用户token
        #验证用户名和密码
        user = db.get_user_by_username(username)
        if not user:
            #用户不存在
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="用户名不存在")
        elif password!=user.password:
            #密码错误
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="用户名密码错误")
        else:
            access_token_expires = timedelta(minutes=ACCESS_USER_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={'sub':username,'guest':0},expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer",'username':username}

@router.post('/login', response_model=Token)
async def get_token_by_phone(form_data:OAuth2PasswordRequestForm = Depends()):
    pass
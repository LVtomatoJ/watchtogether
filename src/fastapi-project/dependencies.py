from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import SECRET_KEY,ALGORITHM,ACCESS_USER_TOKEN_EXPIRE_MINUTES,ACCESS_GUEST_TOKEN_EXPIRE_MINUTES
from .models import TokenData,User
from .db.usemongo import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def check_token_ok(token:str=Depends(oauth2_scheme)):
    #检查token格式是否正确以及是否过期
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        guest: int = payload.get('guest')
        if username is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="令牌错误")
        token_data = TokenData(username=username,guest=guest)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="令牌错误")
    # 检查令牌是否过期
    now = datetime.utcnow()
    expiration = datetime.fromtimestamp(payload["exp"])
    if expiration < now:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="令牌过期")
    return token_data

def check_token_user(token_data:TokenData=Depends(check_token_ok)):
   #已登录用户token
   if token_data.guest:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未登录")
   else:
        #获取用户信息
        user = get_user_by_username(username=token_data.username)
        #检查user是否存在
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户不存在")
        else:
            return user

def check_token_admin(user:User = Depends(check_token_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="非管理员账户")
    return user
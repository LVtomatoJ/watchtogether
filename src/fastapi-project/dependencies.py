from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import SECRET_KEY,ALGORITHM,ACCESS_USER_TOKEN_EXPIRE_MINUTES,ACCESS_GUEST_TOKEN_EXPIRE_MINUTES
from .models import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        guest: int = payload.get('guest')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="令牌错误")
        token_data = TokenData(username=username,guest=guest)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 检查令牌是否过期
    now = datetime.utcnow()
    expiration = datetime.fromtimestamp(payload["exp"])
    if expiration < now:
        raise HTTPException(status_code=401, detail="令牌过期")
    return token_data
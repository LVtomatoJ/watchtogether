from fastapi import Depends,FastAPI
from .routers import users,guest,base,admin,live
from .dependencies import check_token_user,check_token_ok
from .models import User,OutUser

app = FastAPI()

app.include_router(users.router)
app.include_router(guest.router)
app.include_router(base.router)
app.include_router(admin.router)
app.include_router(live.router)

@app.get('/')
async def root(user:User = Depends(check_token_user)):
    return OutUser(**user.dict())
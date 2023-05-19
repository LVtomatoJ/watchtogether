from fastapi import Depends,FastAPI
from .routers import users,guest,base
from .dependencies import get_current_user

app = FastAPI()

app.include_router(users.router)
app.include_router(guest.router)
app.include_router(base.router)
@app.get('/')
async def root(current_user = Depends(get_current_user)):
    return current_user


from fastapi import APIRouter,Depends
from ..dependencies import check_token_admin
from ..models import OutUser
router = APIRouter(prefix='/admin')

@router.get('/check')
async def check_is_admin(user = Depends(check_token_admin)):
    return OutUser(**user.dict())


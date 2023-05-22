from fastapi import APIRouter,Depends
from ..dependencies import check_token_user
from ..models import OutUser
router = APIRouter(prefix='/user')

@router.get('/info')
async def get_user_info(user = Depends(check_token_user)):
    return OutUser(**user.dict()).dict()

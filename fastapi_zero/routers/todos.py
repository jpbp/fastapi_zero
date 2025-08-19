from fastapi import APIRouter

router = APIRouter(prefix='/todos',tags=['TODOS'])

@router.post('/')
async def create_todo():
    ...
    
    
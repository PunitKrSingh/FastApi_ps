from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List,Annotated
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from app.database import get_db

router=APIRouter(
    prefix="/users",
    tags=['Users']
)
db_dep=Annotated[Session,Depends(get_db)]




@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
async def create_user(user:schemas.CreateUser,db:db_dep):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.model_dump(exclude_unset=True))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.User])
async def get_users(db:db_dep):
    users=db.query(models.User).all()
    return users

@router.get('/{id}',response_model=schemas.User)
async def get_user(id:int,db:db_dep):
    user=db.query(models.User).filter(models.User.id==id).first()
    print(user)
    
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id: {id} not found') 

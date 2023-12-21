from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List,Annotated,Optional
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy import func

router= APIRouter(
    prefix="/posts",
    tags=['Posts']
)
db_dep=Annotated[Session,Depends(get_db)]

@router.get("/",response_model=List[schemas.PostOut])
async def test_post(db:db_dep,current_user:int=Depends(oauth2.get_current_user),limit: int=10,skip:int=0,search:Optional[str]=""):
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts=db.query(models.Post).filter(models.Post.user_id==current_user.id).all()
    print(current_user.email)
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.icontains(search)).limit(limit).offset(skip).all()
    print(results)
    
    return results

@router.get('/{id}',response_model=schemas.PostOut)
async def get_post(id:int,db:db_dep,current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.id)
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id: {id} not found') 

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post) 
async def create_post(post:schemas.CreatePost,db:db_dep,current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.id)
    
    new_post=models.Post(user_id=current_user.id,**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post





@router.put('/{id}', status_code=status.HTTP_205_RESET_CONTENT,response_model=schemas.Post)
async def update_post(id: int, updated_post:schemas.UpdatePost, db: db_dep,current_user:int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post:
        # Update only the provided fields that are not None
        update_data = updated_post.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post, field, value)
       
        if post.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized")
        db.commit()
        db.refresh(post)  # Refresh the object in the session
        
        return post
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} not found')

    

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:db_dep,current_user:int=Depends(oauth2.get_current_user)):
    delete_post=db.query(models.Post).filter(models.Post.id==id).first()
    
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    if delete_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized")
    db.delete(delete_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
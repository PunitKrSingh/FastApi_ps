from fastapi import APIRouter,FastAPI,Response,HTTPException,status,Depends
from .. import schemas,database,models,oauth2
from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/vote',
    tags=['Votes']
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
        post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
        if not post:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
        vote_q= db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
        found_vote=vote_q.first()
        
        if vote.dir==1:
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user already voted on this post")
            new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
            db.add(new_vote)
            db.commit() 
            db.refresh(new_vote)
            return {"message":"Succcessfully added vote"} 
        else:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
            vote_q.delete(synchronize_session=False)
            db.commit()
            return {"message":"successfully"}

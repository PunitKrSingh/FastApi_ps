from pydantic import BaseModel,EmailStr,conint
from typing import Optional
from datetime import datetime
class UserBase(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr

class CreateUser(UserBase):
    pass

class User(UserOut):
    
    created_at:datetime
    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email : str
    password : str
class PostBase(BaseModel):
    
    title:str
    content:str
    is_published:bool=True
    

class CreatePost(PostBase):
    pass
    

class UpdatePost(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at:datetime
    user_id:int
    owner:UserOut
    class Config:
        from_attributes=True
class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes=True
    




class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)
   
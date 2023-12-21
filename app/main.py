from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



origins=['*']
# models.Base.metadata.create_all(bind=engine)
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get('/')
def index():
    return {'data':'Index page'}










# db_dep=Annotated[Session,Depends(get_db)]



# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='FASTAPI',user='postgres',password='admin',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("conn.. established!!!!!")
#         break
#     except:
#         print("conn. failed!!!!!!!")
#         time.sleep(5)

    








# *****************************************************************************************************************************************************************************************************

# '''With sql******************************************************************** '''


# @app.get('/posts')
# async def get_posts():
#     cursor.execute(""" SELECT * FROM posts """)
#     posts=cursor.fetchall()
#     return {'posts':posts}

# @app.get('/posts/{id}')
# async def get_post(id:int):
#     cursor.execute(""" SELECT * FROM posts WHERE id=%s""",(id,))
#     post=cursor.fetchone()
    
#     if post:
#         return {'data':post}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id: {id} not found') 

# @app.post('/posts',status_code=status.HTTP_201_CREATED) 
# async def create_post(post:Post):
#     cursor.execute("""INSERT INTO posts (title,content,is_published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.is_published))
#     post=cursor.fetchone()
#     conn.commit()
#     return {'new_post':post}

# @app.put('/posts/{id}', status_code=status.HTTP_205_RESET_CONTENT)
# async def update_post(id: int, updated_post: Post):
#     cursor.execute(
#         """
#         UPDATE posts
#         SET title = %s, content = %s, is_published = %s
#         WHERE id = %s
#         """,
#         (updated_post.title, updated_post.content, updated_post.is_published, id)
#     )
#     conn.commit()
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
#     updated_post_dict = cursor.fetchone()

#     if updated_post_dict:
#         return {'data': updated_post_dict}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} not found')

# @app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id:int):
#     cursor.execute("""DELETE  FROM posts WHERE id = %s Returning *""", (id,))
#     delete_post=cursor.fetchone()
#     conn.commit()
#     if delete_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT) 





# *************************************************************************************************************************************************************************************************





#sqlalchemy orm___________________________________________________________________________________________________________________________________________________________________________________

# @app.get("/posts",response_model=List[schemas.Post])
# async def test_post(db:db_dep):
#     posts=db.query(models.Post).all()
#     return posts

# @app.get('/posts/{id}',response_model=schemas.Post)
# async def get_post(id:int,db:db_dep):
#     post=db.query(models.Post).filter(models.Post.id==id).first()
    
#     if post:
#         return post
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id: {id} not found') 

# @app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schemas.Post) 
# async def create_post(post:schemas.CreatePost,db:db_dep):
#     new_post=models.Post(**post.model_dump())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post





# @app.put('/posts/{id}', status_code=status.HTTP_205_RESET_CONTENT,response_model=schemas.Post)
# async def update_post(id: int, updated_post:schemas.UpdatePost, db: db_dep):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if post:
#         # Update only the provided fields that are not None
#         update_data = updated_post.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(post, field, value)
       
        
#         db.commit()
#         db.refresh(post)  # Refresh the object in the session
        
#         return post
    
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} not found')

    

# @app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id:int,db:db_dep):
#     delete_post=db.query(models.Post).filter(models.Post.id==id).first()
    
#     if delete_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
#     db.delete(delete_post)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT) 

# #____________________________________________________________________________________________________________________________________________________________________________


# #Users________________________________
# @app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
# async def create_user(user:schemas.CreateUser,db:db_dep):
#     hashed_password=utils.hash(user.password)
#     user.password=hashed_password
#     new_user=models.User(**user.model_dump(exclude_unset=True))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/users",status_code=status.HTTP_200_OK,response_model=List[schemas.User])
# async def get_users(db:db_dep):
#     users=db.query(models.User).all()
#     return users

# @app.get('/users/{id}',response_model=schemas.User)
# async def get_user(id:int,db:db_dep):
#     user=db.query(models.User).filter(models.User.id==id).first()
    
#     if user:
#         return user
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id: {id} not found') 


from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db, Session
from .. import models, oauth2, schemas

router = APIRouter(tags=['GET'])

@router.get('/')
def sayHello():
    return {"message":"hello"}

#get post by post id(pid)
@router.get('/{pid}', response_model=schemas.resUserPost)
def getPost(pid: int, db: Session=Depends(get_db), user: oauth2.get_current_user = Depends()):
    user_id  = user.dict().get('user_id')
    get_user = db.query(models.userCred).filter(models.userCred.email==user_id).first()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentails')
    else:
        get_post = db.query(models.posts).filter(models.posts.pid==pid).first()
        if get_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exists")
        posted_by = get_post.id
        post_user = db.query(models.userCred).filter(models.userCred.id==posted_by).first()
        if (post_user.email != user_id) and post_user.acs is True:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Post is Private")
        else:
            return get_post

#get all post
@router.get('/user/posts', response_model=List[schemas.resUserPost])
def getAllPost(db: Session = Depends(get_db), user: oauth2.get_current_user = Depends()):
    user_id  = user.dict().get('user_id')
    get_user = db.query(models.userCred).filter(models.userCred.email==user_id).first()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentails')
    else:
        posts = db.query(models.posts).filter(models.posts.id==get_user.id).all()
        return posts
    

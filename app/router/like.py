from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db, Session
from .. import models, oauth2, schemas

router = APIRouter(tags=['LIKE/UNLIKE'])

@router.post('/post/like/{pid}')
def likePost(pid: int, db: Session = Depends(get_db), user: oauth2.get_current_user = Depends()):
    user_id  = user.dict().get('user_id')
    get_user = db.query(models.userCred).filter(models.userCred.email==user_id).first()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    else:
        get_post = db.query(models.posts).filter(models.posts.pid==pid).first()
        if get_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
        else:
            check_for_like = db.query(models.votes).filter(models.votes.id==get_user.id, models.votes.pid==pid).first()
            post_owner = db.query(models.userCred).filter(models.userCred.id==get_post.id).first()
            
            if post_owner.acs==1 and get_user.email != post_owner.email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Post Not Found(Private Post)")
            
            elif check_for_like is not None:
                print()
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Posted is already liked by you")
            
            likeModel = schemas.postLike(id=get_user.id, pid=get_post.pid)
            liked = models.votes(**likeModel.dict())
            db.add(liked)
            db.commit()
            
            return {pid: "liked"}
            
from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db, Session 
from .. import models, oauth2

router = APIRouter(tags=['DELETE'])

@router.delete('/delete/{pid}')
def deletePost(pid: int, db: Session = Depends(get_db), user: oauth2.get_current_user = Depends()):
    user_id = user.dict().get('user_id')
    get_user = db.query(models.userCred).filter(models.userCred.email==user_id).first()
    
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    else:
        get_post = db.query(models.posts).filter(models.posts.pid==pid).first()
        if get_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
        else:
            if get_post.id != get_user.id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You Are Not Authorized To Perform This Action')
            else:
                db.delete(get_post)
                db.commit()
                raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Posted is removed')
            
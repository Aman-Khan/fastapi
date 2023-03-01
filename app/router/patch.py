from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db, Session
from .. import models, oauth2, schemas
from sqlalchemy import update

router = APIRouter(tags=['PATCH'])

@router.patch('/user/privacy/{acs}')
def privacy(acs: bool, db: Session = Depends(get_db), user: oauth2.get_current_user = Depends()):
    user_id = user.dict().get('user_id')
    get_user = db.query(models.userCred).filter(models.userCred.email==user_id).first()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    else:
        get_user.acs=acs
        db.commit()
        if acs==1:
            return {"Privacy": "Private"}
        else:
            return {"Privacy": "Public"}

from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db, Session
from .. import models, schemas, utils

router = APIRouter(tags=['AUTHENTICATE'])

@router.post('/signup', response_model=schemas.resSignUpInfo)
def signUp(info: schemas.signUpInfo ,db: Session = Depends(get_db)):
    srch_usr = db.query(models.userCred).filter(models.userCred.email==info.email).first()
    if srch_usr is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    else:
        hashed_pwd = utils.hash(info.pwd)
        info.pwd = hashed_pwd 
        new_usr = models.userCred(**info.dict())
        db.add(new_usr)
        db.commit()
        db.refresh(new_usr)
    return new_usr



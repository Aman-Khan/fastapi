from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, oauth2, utils, schemas
from ..database import get_db, Session

router = APIRouter(tags=['POST'])

@router.post('/login', response_model=schemas.resToken)
def login(info: schemas.loginCred ,db: Session = Depends(get_db)):
    email = info.email
    pwd = info.pwd
    table = models.userCred
    usr = db.query(table).filter(table.email==email).first()
    if usr is None or not utils.verify(pwd, usr.pwd):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    else:
        data = {'user_id':email}
        token = oauth2.create_access_token(data)
        resToken = schemas.resToken(token=token, id=usr.id)
        return resToken

@router.post('/post')
def post(postInfo: schemas.userPost, db: Session=Depends(get_db), user: oauth2.get_current_user = Depends()):
    id = user.dict().get('id')
    print(id)
    return {"fsdf", "fsfs"}
from fastapi import APIRouter, Depends, HTTPException, status
from shops_app import schemas
from shops_app.settings.database import get_db
from shops_app.helpers import authentication
from shops_app.exceptions.exception import *
from sqlalchemy.orm import Session
router = APIRouter()


@router.post('/signup')
def signup_endpoint(request: schemas.SignUpIn,
                    db: Session = Depends(get_db)):
    try:
        return authentication.signup(db=db, request=request)
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(se))
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                         detail=str(e))




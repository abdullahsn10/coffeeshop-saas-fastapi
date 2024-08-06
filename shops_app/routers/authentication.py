from fastapi import (APIRouter, Depends,
                     HTTPException, status, Response)

from shops_app import schemas
from shops_app.settings.database import get_db
from shops_app.helpers import authentication
from shops_app.exceptions.exception import *
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/signup', response_model=schemas.ResponseMessage)
def signup_endpoint(request: schemas.SignUpIn, response: Response,
                    db: Session = Depends(get_db)):
    """
        This endpoint is used to sign up a new coffe shop along with admin.
    """
    try:
        registered_admin: schemas.UserCredentialsInResponse = (
            authentication.signup(request=request, db=db))
        response.status_code = status.HTTP_201_CREATED
        return schemas.ResponseMessage(
            detail='Coffee Shop Registered Successfully',
            results=registered_admin,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(se))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@router.post('/login', response_model=schemas.ResponseMessage)
def login(request: schemas.LoginIn, response: Response,
          db: Session = Depends(get_db)):
    """
    This endpoint is used to login a user into the system
    """
    try:
        response.status_code = status.HTTP_200_OK
        token: schemas.Token = (
            authentication.verify_user_credentials_and_gen_token(
                request=request, db=db
            ))
        return schemas.ResponseMessage(
            detail='Login Successfully',
            results=token,
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(se))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

from fastapi import APIRouter, Depends, HTTPException, status, Response

from src import schemas
from src.settings.database import get_db
from src.helpers import authentication
from src.exceptions.exception import *
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/signup", response_model=schemas.UserCredentialsInResponse)
def signup_endpoint(
    request: schemas.SignUpRequestBody,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    This endpoint is used to sign up a new coffe shop along with admin.
    """
    try:
        response.status_code = status.HTTP_201_CREATED
        return authentication.signup(request=request, db=db)
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(se))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/login", response_model=schemas.Token)
def login(
    request: schemas.LoginRequestBody, response: Response, db: Session = Depends(get_db)
):
    """
    This endpoint is used to login a user into the system
    """
    try:
        response.status_code = status.HTTP_200_OK
        return authentication.verify_user_credentials_and_gen_token(
            request=request, db=db
        )
    except ShopsAppException as se:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(se))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

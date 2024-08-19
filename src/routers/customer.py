from fastapi import APIRouter, Depends, Response, HTTPException, status
from src import schemas
from sqlalchemy.orm import Session
from src.settings.database import get_db
from src.security.oauth2 import require_role
from src.models.user import UserRole
from src.helpers import customer
from src.exceptions.exception import ShopsAppException

router = APIRouter(
    tags=["Customers"],
    prefix="/customer",
)

# setup customer endpoints

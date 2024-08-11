from typing import Optional
from fastapi import status


class ShopsAppException(Exception):
    """
    Custom exception class for ShopsApp
    Can be used to raise exceptions in the application of type:
    - Not Found Exception with status code = 404
    - Bad Request Exception with status code = 400
    - Unauthorized Exception with status code = 401
    - Conflict Exception with status code = 409
    - Any General Exception
    """

    def __init__(
        self, message: str, status_code: Optional[int] = status.HTTP_400_BAD_REQUEST
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

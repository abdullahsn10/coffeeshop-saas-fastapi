from typing import Any

from pydantic import BaseModel


class ResponseMessage(BaseModel):
    detail: str
    results: Any

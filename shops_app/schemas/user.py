from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_no: str
    password: str

    class Config:
        orm_mode = True


class UserCredentialsInResponse(BaseModel):
    email: str
    phone_no: str

    class Config:
        orm_mode = True

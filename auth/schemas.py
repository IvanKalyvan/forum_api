from fastapi_users import schemas
from typing import Optional
from pydantic.version import VERSION as PYDANTIC_VERSION
from pydantic import ConfigDict, EmailStr

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

class UserRead(schemas.BaseUser[int]):

    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    if PYDANTIC_V2:
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:

        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):

    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
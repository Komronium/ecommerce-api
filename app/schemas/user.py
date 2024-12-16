from pydantic import BaseModel, EmailStr, UUID4


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserOut(UserBase):
    id: UUID4
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access: str
    refresh: str
    token_type: str = 'bearer'


class RefreshToken(BaseModel):
    refresh: str

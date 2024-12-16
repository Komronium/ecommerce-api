from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token, RefreshToken
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.api.deps import get_db_dependency


router = APIRouter()


@router.post('/signup', response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db_dependency)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login', response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db_dependency)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid email or password')

    access_token = create_access_token(data={'sub': user.email})
    refresh_token = create_refresh_token(data={'sub': user.email})
    return {'access': access_token, 'refresh': refresh_token, 'token_type': 'bearer'}


@router.post('/refresh', response_model=Token)
def refresh_token(refresh_data: RefreshToken):
    try:
        payload = jwt.decode(refresh_data.refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(data={"sub": email})
    new_refresh_token = create_refresh_token(data={"sub": email})
    return {"access": access_token, "refresh": new_refresh_token, "token": "bearer"}

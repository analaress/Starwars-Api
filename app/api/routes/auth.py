from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.services.auth_service import authenticate_user
from sqlalchemy.orm import Session

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User 
from app.schemas.user import UserCreate
from app.core.security import hash_password #

router = APIRouter()

@router.post("/register", status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.username == user_in.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")

    hashed = hash_password(user_in.password)

    new_user = User(
        username=user_in.username,
        password_hash=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.id, "username": new_user.username, "msg": "Usuário criado!"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = authenticate_user(db, form.username, form.password)
    if not token:
        raise HTTPException(status_code=401)
    return {"access_token": token, "token_type": "bearer"}

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return create_access_token({"sub": user.username})

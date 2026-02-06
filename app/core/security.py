from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, status
from fastapi.requests import Request
from app.db.session import get_db
from app.db.utils import get_user_by_username
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from typing import Optional

class OAuth2PasswordJWT(OAuth2PasswordBearer):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict] = None,
        auto_error: bool = True,
    ):
        super().__init__(
            tokenUrl=tokenUrl,
            scopes=scopes,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str | None = request.headers.get("X-Forwarded-Authorization")

        if not authorization:
            authorization: str | None = request.headers.get("Authorization")

        print(authorization)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "JWT"},
                )
            else:
                return None
        return param


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordJWT(tokenUrl="login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": int(expire.timestamp()),
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            username = payload.get("email")

        if username is None:
            raise HTTPException(status_code=401, detail="Token sem identificação")
        
        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
            
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception as e:
        print(f"DEBUG Erro: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Erro de autenticação: {str(e)}")
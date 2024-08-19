from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt

from app.db.models.userModel import User
from app.utils.core.config import settings
from app.schemas.token import TokenData, Token

blacklist = {}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def createToken(user: User) -> Token:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "account_type": user.type}, expires_delta=access_token_expires
    )
    token = Token(access_token=access_token)
    return token

def verify_token(token: str, credentials_exception) -> TokenData:
    if token in blacklist and blacklist[token] > datetime.now():
        raise credentials_exception
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")
        account_type: str = payload.get("account_type")

        expiration_time = datetime.fromtimestamp(exp)
        token_expired = expiration_time < datetime.now()

        if username is None or exp is None or account_type is None or token_expired:
            raise credentials_exception

        token_data = TokenData(email=username, exp=datetime.fromtimestamp(exp), account_type=account_type)
    except JWTError:
        raise credentials_exception
    return token_data


def add_token_to_blacklist(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    exp = datetime.fromtimestamp(payload["exp"])
    blacklist[token] = exp
    clean_blacklist()


def clean_blacklist():
    now = datetime.now()
    expired_tokens = [token for token, exp in blacklist.items() if exp <= now]
    for token in expired_tokens:
        del blacklist[token]

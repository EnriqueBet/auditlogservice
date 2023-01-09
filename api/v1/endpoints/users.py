from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from api.v1.utils import common
from api.v1 import config
from api.v1.models import Token, TokenData, RegisteredUser
from api.v1.database import DatabaseClient as db_client

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authToken")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def authenticate_user(username: str, pwd: str):
    user = get_user(username)
    if not user or not verify_password(pwd, user.hashed_password):
        return False
    return user

def verify_password(str_pwd: str, hash_pwd: str) -> bool:
    result = pwd_context.verify(str_pwd, hash_pwd)
    print(result)
    return result

def get_user(username: str):
    user_map = db_client.get_instance().database["users"].find_one({'username': username})
    if user_map:
        user_map["_id"] = str(user_map['_id'])
        return RegisteredUser(**user_map)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials were not validated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.HASH_ALGO)
        if (username := str(payload.get("sub"))) is None:
            raise user_exception
        token_data = TokenData(username=username)
    except JWTError as error:
        raise user_exception
    if (user := get_user(username=token_data.username)) is None:
        raise user_exception

    if user.disabled:
        raise HTTPException(status_code=400, detail='Your user is disabled, please contact the system admin')
    return user

@router.post("/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not (user := authenticate_user(form_data.username, form_data.password)):
        raise HTTPException(status_code=400, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = common.create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

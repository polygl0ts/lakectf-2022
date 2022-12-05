# Copyright (c) 2022 Junior Dev

# References:
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt
# https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Union
import importlib.resources
import hashlib
import html
import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from redis import Redis
from rq import Queue

HASHED_ADMIN_PASSWORD = os.getenv('HASHED_ADMIN_PASSWORD')
FLAG = os.getenv("FLAG")

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_dbs = {}


def init_instance(instance):
    fake_dbs[instance] = {
        "instance": instance,
        "users": {
            "admin": {
                "username": "admin",
                "full_name": "Administrator",
                "email": "admin@epfl.ch",
                "hashed_password": HASHED_ADMIN_PASSWORD,
                "disabled": False,
                "admin": True,
            },
        },
        "lines": [
            {
                "creator_username": "admin",
                "description": "Toilet Paper",
                "amount": Decimal("34.555"),
            },
        ],
    }


def destroy_instance(instance):
    del fake_dbs[instance]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    instance: Union[str, None] = None
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    admin: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class Line(BaseModel):
    description: str
    amount: Decimal
    creator_username: str


pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db["users"]:
        user_dict = db["users"][username]
        return UserInDB(**user_dict)


def get_line_by_nr(db, line_nr: int):
    if line_nr < len(db["lines"]):
        line_dict = db["lines"][line_nr]
        return Line(**line_dict)


def get_all_lines(db):
    for line_dict in db["lines"]:
        yield Line(**line_dict)


def add_line(db, line: Line):
    db["lines"].append(line.dict())


async def get_db(instance: str):
    db = fake_dbs.get(instance)
    if db is None:
        raise HTTPException(404, detail="No such instance")
    return db


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        instance: str = payload.get("instance")
        if username is None:
            raise credentials_exception
        token_data = TokenData(instance=instance, username=username)
    except JWTError:
        raise credentials_exception
    if db["instance"] != instance:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/{instance}/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    db=Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    fingerprint = secrets.token_hex(32)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "jti": hashlib.sha3_256(fingerprint.encode()).hexdigest(),
            "instance": db["instance"],
        },
        expires_delta=access_token_expires,
    )

    response.set_cookie(
        "__Host-Fgp",
        fingerprint,
        path="/",
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/{instance}/register")
async def register(
    db=Depends(get_db),
    username: str = Form(),
    full_name: str = Form(),
    email: EmailStr = Form(),
    password: str = Form(),
):
    if username in db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username is already taken",
        )
    db["users"][username] = {
        "username": username,
        "full_name": full_name,
        "email": email,
        "hashed_password": get_password_hash(password),
        "disabled": False,
        "admin": False,
    }


@app.get("/{instance}/flag")
async def flag(
    response: Response, current_user: User = Depends(get_current_active_user)
):
    response.headers["Access-Control-Allow-Origin"] = "127.0.0.1"
    if current_user.admin:
        return FLAG
    else:
        return "EPFL{404_F1ag_n0t_Found}"


@app.get("/{instance}/destroy")
async def destroy(
    db=Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    if current_user.admin:
        destroy_instance(db["instance"])


@app.get("/{instance}/lines/list", response_model=List[Line])
async def lines_list(
    db=Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    return list(get_all_lines(db))


@app.get("/{instance}/lines/display")
async def lines_display(
    db=Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    response = "<div>"
    for line in get_all_lines(db):
        response += f"<p>{line.amount} | {line.description} | {line.creator_username}"
    return response


@app.post("/{instance}/lines/add")
async def lines_add(
    db=Depends(get_db),
    description: str = Form(),
    amount: Decimal = Form(),
    current_user: User = Depends(get_current_active_user),
):
    add_line(
        db,
        Line(
            description=html.escape(description),
            amount=amount,
            creator_username=current_user.username,
        ),
    )


@app.get("/{instance}")
async def instance_top(instance):
    return RedirectResponse(f"/{instance}/index.html")


INDEX_HTML = importlib.resources.read_binary(__name__, "index.html")


@app.get("/{instance}/index.html")
async def instance_index(instance, _=Depends(get_db)):
    return HTMLResponse(INDEX_HTML)


from . import bot

q = Queue(connection=Redis.from_url("redis://redis:6379"))


@app.get("/")
@app.get("/index.html")
async def index():
    instance = secrets.token_urlsafe()
    init_instance(instance)
    q.enqueue(bot.visit, instance)
    return RedirectResponse(f"/{instance}/index.html")

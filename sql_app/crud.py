from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.sql.expression import delete

from .import database
from .import models, schemas
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "7049df34ffff4ea67ada6caa17b5d37941ec527c25588062afbb605d74cd2f8e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, email: str, data: schemas.UserUpdate):
    dict_data = dict(data)
    current_user = get_user(db, email=email)
    for key in list(dict_data):
        if dict_data[key] is None:
            del dict_data[key]
    db.query(models.User).filter(models.User.email == email).update(
        dict_data, synchronize_session="fetch")
    db.commit()
    db.refresh(current_user)
    return current_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# def upgrade_user(db: Session, email: str):
#     hasil = db.query(models.Product).filter(models.User.email == email).first()
#     current_user = get_user(db, email=email)
#     db.query(models.User).filter(models.User.email == email).update(synchronize_session="fetch", status = "member")
#     db.commit()
#     db.refresh(current_user)
#     return current_user

def get_products(db: Session, product_id: int):
    hasil = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    return hasil

def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_products_name(db: Session, nama_product: str):
    hasil = db.query(models.Product).filter(models.Product.nama_product == nama_product).first()
    return hasil

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        email: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    # user = schemas.User(id=user_model.id, username=user_model.username, email=user_model.email,
    #                     tanggal_lahir=user_model.tanggal_lahir, alamat=user_model.alamat, no_telp=user_model.no_telp, status=user_model.status)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user

def upgrade_user(db: Session, email: str, user: schemas.UserUpdate):
    current_user = get_user(db, email=email)
    # db_order = get_order(db, order.id_pesanan)
    upgrade = {
        "status": "member"
    }
    db.query(models.User).filter(models.User.email == user.email).update(dict(upgrade))
    db.commit()
    db.refresh(current_user)
    return current_user

def create_member(db: Session, member: schemas.MemberCreate):
    # hashed_password = get_password_hash(user.password)
    current_user = get_user(db, email=email)
    db_user = models.Member(member_id=current_user.id, poin= 0, benefit= "belum ada", pelanggan_id=current_user.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .import crud, models, schemas
from .database import get_db, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.post("/token", response_model=schemas.Token, tags=["authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"username": user.username, "email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=List[schemas.User], tags=["user"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/me/", response_model=schemas.User, tags=["user"])
def read_users_me(current_user: schemas.User = Depends(crud.get_current_user)):
    return current_user

# @app.patch("/users/{email}", tags=["user"])
# def upgrade_user(data: schemas.UserUpdate, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(crud.get_current_active_user)):
#     users = crud.upgrade_user(db, current_user.email)
#     return users

@app.get("/product/{product_id}", response_model=schemas.Product, tags=["product"])
def read_products(product_id:int, db: Session = Depends(get_db)):
    products = crud.get_products(db, product_id)
    return products

@app.get("/product/", response_model=List[schemas.Product], tags=["product"])
def read_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_all_products(db, skip=skip, limit=limit)
    return products

# @app.get("/product/{nama_product}", response_model=schemas.Product, tags=["product"])
# def read_products_name(nama_product:str, db: Session = Depends(get_db)):
#     products = crud.get_products_name(db, nama_product)
#     return products

@app.patch("/users/", response_model = schemas.User, tags=["user"])
def upgrade_user(email:str, db: Session = Depends(get_db)):
    user = crud.upgrade_user(db, email)# tambahin exception kalau salah
    return user

@app.post("/members/", response_model=schemas.MemberBase, tags=["member"])
def create_member(email:str, db: Session = Depends(get_db)):
    return crud.create_member(db=db, email=email)

@app.get("/users/{email}", response_model=schemas.User, tags=["user"])
def read_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
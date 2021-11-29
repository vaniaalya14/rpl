from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    tanggal_lahir: date
    alamat: str
    status: Optional[str]
    no_telp: str


class UserUpdate(BaseModel):
    email: Optional[str]
    username: Optional[str]
    tanggal_lahir: Optional[date]
    alamat: Optional[str]
    status: Optional[str]
    no_telp: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    nama_product: Optional[str]
    harga: Optional[int]
    deskripsi: Optional[str]
    stok: Optional[int]
    gambar: Optional[str]

class Product(ProductBase):
    product_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class MemberBase(BaseModel):
    poin: int
    benefit: str
    pelanggan_id: int

class MemberCreate(MemberBase):
    member_id: int
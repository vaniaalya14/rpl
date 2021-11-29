from sqlalchemy import Boolean, Column, ForeignKey, BigInteger, String, Date, Integer
from sqlalchemy.sql.sqltypes import Enum
from .database import Base


class User(Base):
    __tablename__ = "pelanggan"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    username = Column(String(100))
    tanggal_lahir = Column(Date)
    alamat = Column(String(255))
    no_telp = Column(String(20))
    status = Column(String(10), nullable=True)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

class Product(Base):
    __tablename__ = "product"

    product_id = Column(BigInteger, primary_key=True)
    nama_product = Column(String(255))
    harga = Column(Integer)
    deskripsi = Column(String(255))
    stok = Column(Integer)
    gambar = Column(String(255))

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

class Member(Base):
    __tablename__ = "member"

    member_id = Column(Integer, primary_key=True, index=True)
    poin = Column(Integer)
    benefit = Column(String(255))
    pelanggan_id = Column(BigInteger)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
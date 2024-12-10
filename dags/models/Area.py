from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from .base import Base  # 引用分離出的 Base


from utils.code_enum import  city_t

class Area(Base):

    __tablename__ = "area"
    id = Column(Integer, primary_key=True)
    City = Column(city_t, nullable=True)

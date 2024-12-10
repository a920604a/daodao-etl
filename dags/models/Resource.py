from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from utils.code_enum import cost_t, age_t
from .base import Base  # 引用分離出的 Base



class Resource(Base):
    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_by_user_id = Column(String, ForeignKey("users.uuid"))
    image_url = Column(String(255))
    cost = Column(cost_t, default='free')
    age = Column(age_t, default = 'other')
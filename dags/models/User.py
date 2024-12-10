from sqlalchemy import create_engine, Column, TIMESTAMP, ARRAY, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from utils.code_enum import education_stage_t, gender_t

from .base import Base  # 引用分離出的 Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True, nullable=False)
    gender = Column(gender_t, nullable=True)
    education_stage = Column(education_stage_t, default='other')
    role_list = Column(ARRAY(String))
    contact_id = Column(Integer, ForeignKey("contact.id"))
    location_id = Column(Integer, ForeignKey("location.id"))
    basic_info_id = Column(Integer, ForeignKey("basic_info.id"))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

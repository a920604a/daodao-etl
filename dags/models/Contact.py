from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from .base import Base  # 引用分離出的 Base


# 定義 Contact 類
class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    google_id = Column(String(255), nullable=True)
    photo_url = Column(Text, nullable=True)
    is_subscribe_email = Column(Boolean, nullable=True)
    email = Column(String(255), nullable=True)
    ig = Column(String(255), nullable=True)
    discord = Column(String(255), nullable=True)
    line = Column(String(255), nullable=True)
    fb = Column(String(255), nullable=True)

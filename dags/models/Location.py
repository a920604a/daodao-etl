from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from .base import Base  # 引用分離出的 Base



class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=True)
    is_taiwan = Column(Boolean, nullable=True)
    region = Column(String(64), nullable=True)

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData, CHAR
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from .base import Base  # 引用分離出的 Base



class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    area_id = Column(Integer, ForeignKey("area.id"), nullable=True)
    isTaiwan = Column(Boolean, nullable=True)
    region = Column(CHAR(64), nullable=True)

    # 與 Area 建立一對一關聯
    area = relationship("Area", back_populates="locations")
    # 與 user 關聯
    user = relationship("Users", back_populates="location")

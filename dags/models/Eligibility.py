from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from utils.code_enum import qualifications_t

from .base import Base  # 引用分離出的 Base


# 定義 Eligibility 類
class Eligibility(Base):
    __tablename__ = "eligibility"
    id = Column(Integer, primary_key=True)
    qualifications = Column(qualifications_t, nullable=True)
    qualification_file_path = Column(String(255), nullable=True)

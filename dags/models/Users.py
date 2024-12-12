from sqlalchemy import create_engine, Column, TIMESTAMP, ARRAY, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData, Date
from sqlalchemy.dialects.postgresql import  UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from utils.code_enum import education_stage_t, gender_t

from .base import Base  # 引用分離出的 Base
import uuid

    
# User 表
class Users(Base):
    __tablename__ = "users"

    # 欄位定義
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)  # Primary Key
    _id = Column(Text, nullable=False, unique=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)

    gender = Column("gender", gender_t, nullable=True)  # 對應 gender_t
    language = Column(String(255), nullable=True)
    education_stage = Column(
        "education_stage", String, default="other", nullable=True
    )  # Default 設定為 'other'
    tag_list = Column("tagList", String, nullable=True)
    contact_id = Column(Integer, ForeignKey("contact.id"), nullable=True)  # 外鍵
    is_open_location = Column(Boolean, nullable=True)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=True)  # 外鍵
    nickname = Column(String(255), nullable=True)
    role_list = Column("role_list", ARRAY(String), nullable=True)  # 角色類型
    is_open_profile = Column(Boolean, nullable=True)
    birth_day = Column("birthDay", Date, nullable=True)
    basic_info_id = Column(Integer, ForeignKey("basic_info.id"), nullable=True)  # 外鍵
    created_by = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_by = Column(String(255), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # 定義外鍵關聯
    contact = relationship("Contact", back_populates="users")
    location = relationship("Location", back_populates="users")
    basic_info = relationship("BasicInfo", back_populates="users")
    resource = relationship("Resource", back_populates="users")

from sqlalchemy import create_engine, Column, Integer, ARRAY, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from utils.code_enum import want_to_do_list_t

from .base import Base  # 引用分離出的 Base


# 定義 BasicInfo 類
class BasicInfo(Base):
    __tablename__ = "basic_info"
    id = Column(Integer, primary_key=True)
    self_introduction = Column(Text, nullable=True)
    share_list = Column(Text, nullable=True)
    want_to_do_list = Column(ARRAY(want_to_do_list_t), nullable=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)

from sqlalchemy import create_engine, Column, Integer, ARRAY, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from utils.code_enum import want_to_do_list_t

from .base import Base  # 引用分離出的 Base


class BasicInfo(Base):
    __tablename__ = "basic_info"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    self_introduction = Column(String, nullable=True)
    share_list = Column("share_list", String, nullable=True)  # text
    want_to_do_list = Column("want_to_do_list", ARRAY(String), nullable=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)

    # 與 Users 關聯
    users = relationship("Users", back_populates="basic_info")

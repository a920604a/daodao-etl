from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from utils.code_enum import partnerEducationStep_t
from .base import Base  # 引用分離出的 Base


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text)
    group_type = Column(Enum(GroupTypeEnum), default='other')
    area_id = Column(Integer, ForeignKey('location.id'))
    created_by = Column(String, ForeignKey("users.uuid"))
    isGrouping = Column(Boolean)
    partnerEducationStep = Column(partnerEducationStep_t, default='other')

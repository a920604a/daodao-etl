from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, Enum, Table, MetaData
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from utils.code_enum import partnerEducationStep_t, group_type_t
from .base import Base  # 引用分離出的 Base



class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    photoURL = Column(String(255))
    photoALT = Column(String(255))
    category = Column(Text)
    group_type = Column(Enum('other', name='group_type_t'), default='other')
    partnerEducationStep = Column(Enum('other', name='partnerEducationStep_t'), default='other')
    description = Column(String(255))
    area_id = Column(Integer)
    isGrouping = Column(Boolean)
    updatedDate = Column(Date)
    time = Column(Time)
    partnerStyle = Column(Text)
    tagList = Column(Text)
    created_at = Column(Date)
    created_by = Column(UUID)
    updated_at = Column(Date)
    updated_by = Column(String(255))
    motivation = Column(Text)
    Contents = Column(Text)
    expectation_result = Column(Text)
    Notice = Column(Text)
    group_daedline = Column(Date)
    hold_time = Column(Time)
    isOnline = Column(Boolean)
    TBD = Column(Boolean)
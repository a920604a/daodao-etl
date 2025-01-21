# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from .base import Base  # 引用分離出的 Base


class UserIdentity(Base):
    __tablename__ = 'user_identities'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    identity_id = Column(Integer, ForeignKey('identity.id'), primary_key=True)

    user = relationship("Users", backref="user_identities")
    identity = relationship("Identity", backref="user_identities")
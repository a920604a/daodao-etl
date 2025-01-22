from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from .base import Base  # 引用分離出的 Base


# 定義 Position 類型
class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    # 與 UserPosition 關聯
    users = relationship("Users",secondary="user_positions",back_populates="identities", overlaps="user_positions")


    def __repr__(self):
        return f"<Position(id={self.id}, name='{self.name}')>"

# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from .base import Base  # 引用分離出的 Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主鍵")
    milestone_id = Column(Integer, ForeignKey("milestone.id", ondelete="CASCADE"), nullable=False, comment="里程碑 ID")
    name = Column(String(255), comment="任務名稱")
    description = Column(Text, comment="任務描述")
    start_date = Column(Date, comment="開始日期")
    end_date = Column(Date, comment="結束日期")
    is_completed = Column(Boolean, default=False, comment="是否完成")
    is_deleted = Column(Boolean, default=False, comment="是否已刪除")
    created_at = Column(TIMESTAMP, default="now()", comment="建立時間")
    updated_at = Column(TIMESTAMP, default="now()", onupdate="now()", comment="更新時間")

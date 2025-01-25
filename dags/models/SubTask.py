# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from .base import Base  # 引用分離出的 Base

class DayEnum(enum.Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"



class SubTask(Base):
    __tablename__ = "subtask"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主鍵")
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), nullable=False, comment="任務 ID")
    name = Column(String(255), comment="子任務名稱")
    days_of_week = Column(ARRAY(Enum(DayEnum)), comment="重複的星期")
    is_completed = Column(Boolean, default=False, comment="是否完成")
    is_deleted = Column(Boolean, default=False, comment="是否已刪除")
# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, ARRAY, Text
from utils.code_enum import day_t
from .base import Base  # 引用分離出的 Base
from sqlalchemy.orm import relationship

 

class SubTask(Base):
    __tablename__ = "subtask"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主鍵")
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), nullable=False, comment="任務 ID")
    name = Column(String(255), comment="子任務名稱")
    description=Column(Text)
    days_of_week = Column(ARRAY(day_t), comment="重複的星期")
    is_completed = Column(Boolean, default=False, comment="是否完成")
    is_deleted = Column(Boolean, default=False, comment="是否已刪除")
    
    task = relationship("Task", back_populates="subtasks")

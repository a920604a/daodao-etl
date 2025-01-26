from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean, TIMESTAMP
from .base import Base  # 引用分離出的 Base
from sqlalchemy.orm import relationship
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


    # 關聯
    milestone = relationship("Milestone", back_populates="tasks")
    subtasks = relationship("SubTask", back_populates="task", cascade="all, delete-orphan")

    # 這裡是使用 primaryjoin 與 secondary 來讓 Task 透過 Milestone 與 Project 關聯
    project = relationship(
        "Project",
        secondary="milestone",  # 使用 milestone 作為中介表
        back_populates="tasks",
    )
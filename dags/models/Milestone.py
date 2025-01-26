
# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .base import Base  # 引用分離出的 Base


class Milestone(Base):
    __tablename__ = "milestone"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主鍵")
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"), nullable=False, comment="專案 ID")

    start_date = Column(Date, comment="開始日期")
    end_date = Column(Date, CheckConstraint("start_date < end_date", name="check_start_end_date"), comment="結束日期")
    interval = Column(Integer, CheckConstraint("interval > 0", name="check_interval_positive"), comment="週期間隔（單位：週）")
    
    # 關聯
    project = relationship("Project", back_populates="milestones")
    tasks = relationship("Task", back_populates="milestone", cascade="all, delete-orphan")

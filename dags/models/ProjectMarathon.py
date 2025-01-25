# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from .base import Base  # 引用分離出的 Base



class ProjectMarathon(Base):
    __tablename__ = "project_marathon"
    __table_args__ = (
        CheckConstraint("status IN ('Pending', 'Approved', 'Rejected')", name="check_status"),  # 檢查約束
        UniqueConstraint("project_id", "marathon_id", name="unique_project_marathon"),  # 唯一約束
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="使用 UUID 作為主鍵")
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"), nullable=False, comment="專案 ID，指向 project 表的 id")
    marathon_id = Column(UUID(as_uuid=True), ForeignKey("marathon.id", ondelete="CASCADE"), nullable=False, comment="馬拉松 ID，指向 marathon 表的 id")
    project_registration_date = Column(TIMESTAMP, default="now()", comment="專案報名此馬拉松的日期")
    status = Column(String(50), comment="專案報名的審核狀態")
    feedback = Column(Text, comment="評審意見或備註")
    created_at = Column(TIMESTAMP, default="now()", comment="建立時間")
    updated_at = Column(TIMESTAMP, default="now()", onupdate="now()", comment="更新時間")
# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from .base import Base  # 引用分離出的 Base
from code_enum import motivation_t, policy_t, presentation_t

# 定義新表結構
class Project(Base):
    __tablename__ = 'project'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    img_url = Column(String(255))
    topic = Column(String(255))
    project_description = Column(Text)
    motivation = Column(ARRAY(motivation_t))
    motivation_description = Column(Text)
    goal = Column(String(255))
    content = Column(Text)
    policy = Column(ARRAY(policy_t))
    policy_description = Column(Text)
    resource_name = Column(ARRAY(Text))
    resource_url = Column(ARRAY(Text))
    presentation = Column(ARRAY(presentation_t))
    presentation_description = Column(Text)
    is_public = Column(Boolean, default=False)
    status = Column(String(50), CheckConstraint("status IN ('Ongoing', 'Completed', 'Not Started', 'Canceled')"), default='Not Started')
    created_at = Column(TIMESTAMP, default='now()')
    created_by = Column(Integer)
    updated_at = Column(TIMESTAMP, default='now()', onupdate='now()')
    updated_by = Column(Integer)
    version = Column(Integer)

    milestones = relationship("Milestone", back_populates="project")
    tasks = relationship("Task", back_populates="project")
# 用戶身份聯接表
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from .base import Base  # 引用分離出的 Base
from code_enum import motivation_t, policy_t, presentation_t

class Marathon(Base):
    __tablename__ = 'marathon'

    __table_args__ = (
        Index("idx_marathon_start_date", "start_date"),  # 建立索引
        CheckConstraint("registration_status IN ('Open', 'Closed', 'Pending', 'Full')", name="check_registration_status"),  # 檢查約束
    )


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="使用 UUID 作為主鍵")
    event_id = Column(String(50), nullable=False, unique=True, comment="活動代碼，例如 '2024S1'")
    title = Column(String(255), nullable=False, comment="活動標題")
    description = Column(Text, comment="活動描述")
    start_date = Column(Date, nullable=False, comment="馬拉松的報名開始日期")
    end_date = Column(Date, nullable=False, comment="活動結束日期")
    registration_status = Column(String(50), comment="活動的整體報名狀態")
    people_number = Column(Integer, comment="報名人數上限")
    registration_start_date = Column(Date, comment="報名開放日期")
    eligibility_id = Column(Integer, ForeignKey("eligibility.id"), comment="收費計劃")
    is_public = Column(Boolean, default=False, comment="是否公開")
    created_by = Column(Integer, ForeignKey("users.id"), comment="主辦者 (可選)")
    created_at = Column(TIMESTAMP, default='now()', comment="建立時間")
    updated_at = Column(TIMESTAMP, default='now()', onupdate='now()', comment="更新時間")


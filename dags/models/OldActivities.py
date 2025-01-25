from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, Time, ForeignKey, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

class OldActivities(Base):
    __tablename__ = 'old_activities'
    mongo_id = Column(Text, primary_key=True)
    userId = Column(Text)
    title = Column(Text)
    photoURL = Column(Text)
    photoAlt = Column(Text)
    category = Column(Text)
    area = Column(Text)
    time = Column(Text)
    partnerStyle = Column(Text)
    partnerEducationStep = Column(Text)
    description = Column(Text)
    tagList = Column(Text)
    isGrouping = Column(Boolean)
    createdDate = Column(Text)
    updatedDate = Column(Text)
    created_at = Column(Text)
    created_by = Column(Text)
    updated_at = Column(Text)
    updated_by = Column(Text)
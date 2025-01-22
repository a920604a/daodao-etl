from sqlalchemy import Column, Integer, String, Text, Date, Boolean, Time, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from .base import Base  # 引用分離出的 Base
from utils.code_enum import partnerEducationStep_t, group_type_t

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    photoURL = Column('photo_url', String(255))
    photoALT = Column('photo_alt',String(255))
    category = Column(Text)
    
    group_type = Column(ARRAY(group_type_t), default='other')
    partnerEducationStep = Column('partner_education_step', ARRAY(partnerEducationStep_t), default='other')
    
    description = Column(String(255))
    area_id = Column(Integer)
    isGrouping = Column('is_grouping', Boolean)
    createdDate = Column('created_date', Date)
    updatedDate = Column('updated_date', Date)
    time = Column(Time)
    partnerStyle = Column('partner_style', Text)
    tagList = Column('tag_list', Text)
    
    created_at = Column(Date, default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))
    
    updated_at = Column(Date)
    updated_by = Column(String(255))
    
    motivation = Column(Text)
    contents = Column(Text)
    expectation_result = Column(Text)
    notice  = Column(Text)
    group_deadline = Column(Date)
    hold_time = Column(Time)
    is_online = Column(Boolean)
    TBD = Column(Boolean)
    
    # Relationships
    created_by_user = relationship("Users", back_populates="groups_created")
    user_join_group = relationship("UserJoinGroup", back_populates="group")
    
    def __repr__(self):
        return f"<Group(id={self.id}, title={self.title})>"
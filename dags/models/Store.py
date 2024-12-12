from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Store(Base):
    __tablename__ = 'Store'
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # UUID for unique identification
    # uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=True)
    # URL fields
    image_url = Column(String(255), nullable=True)
    
    # Text fields
    author_list = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    
    # Content fields
    ai_summary = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Store(id={self.id}, name='{self.name}', created_at={self.created_at})>"
    
    @classmethod
    def from_dict(cls, data):
        """
        從字典創建 Store 實例
        """
        return cls(
            uuid=data.get('uuid'),
            image_url=data.get('image_url'),
            author_list=data.get('author_list'),
            tags=data.get('tags'),
            name=data.get('name'),
            ai_summary=data.get('ai_summary'),
            description=data.get('description'),
            content=data.get('content'),
            created_at=data.get('created_at')
        )
    
    def to_dict(self):
        """
        將 Store 實例轉換為字典
        """
        return {
            'id': self.id,
            'uuid': str(self.uuid) if self.uuid else None,
            'image_url': self.image_url,
            'author_list': self.author_list,
            'tags': self.tags,
            'name': self.name,
            'ai_summary': self.ai_summary,
            'description': self.description,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
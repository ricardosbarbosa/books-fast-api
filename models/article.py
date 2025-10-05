from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .base import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, index=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    published = Column(String(10), default="draft")  # draft, published, archived
    reading_time = Column(Integer, nullable=True)  # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', author='{self.author}')>"

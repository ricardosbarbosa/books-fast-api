from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Article title")
    author: str = Field(..., min_length=1, max_length=100, description="Article author")
    content: str = Field(..., min_length=1, description="Article content")
    summary: Optional[str] = Field(None, description="Article summary")
    category: Optional[str] = Field(None, max_length=50, description="Article category")
    tags: Optional[str] = Field(None, max_length=500, description="Comma-separated tags")
    published: str = Field("draft", description="Publication status: draft, published, archived")
    reading_time: Optional[int] = Field(None, ge=1, description="Reading time in minutes")

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[str] = Field(None, max_length=500)
    published: Optional[str] = None
    reading_time: Optional[int] = Field(None, ge=1)

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse]
    total: int
    page: int
    size: int

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    author: str = Field(..., min_length=1, max_length=100, description="Book author")
    description: Optional[str] = Field(None, description="Book description")
    isbn: Optional[str] = Field(None, max_length=20, description="ISBN number")
    price: Optional[float] = Field(None, ge=0, description="Book price")
    publication_date: Optional[datetime] = Field(None, description="Publication date")

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=20)
    price: Optional[float] = Field(None, ge=0)
    publication_date: Optional[datetime] = None

class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class BookListResponse(BaseModel):
    books: list[BookResponse]
    total: int
    page: int
    size: int

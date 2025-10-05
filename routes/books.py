from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Book, User
from schemas import BookCreate, BookUpdate, BookResponse, BookListResponse
from auth import get_current_active_user

router = APIRouter()

@router.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Create a new book"""
    # Check if ISBN already exists
    if book.isbn:
        existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="ISBN already exists")
    
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/books/", response_model=BookListResponse)
def get_books(
    skip: int = Query(0, ge=0, description="Number of books to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of books to return"),
    search: Optional[str] = Query(None, description="Search in title and author"),
    db: Session = Depends(get_db)
):
    """Get all books with pagination and search"""
    query = db.query(Book)
    
    # Apply search filter
    if search:
        query = query.filter(
            (Book.title.contains(search)) | 
            (Book.author.contains(search))
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    books = query.offset(skip).limit(limit).all()
    
    return BookListResponse(
        books=books,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Update a book"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if ISBN already exists (excluding current book)
    if book_update.isbn:
        existing_book = db.query(Book).filter(
            Book.isbn == book_update.isbn,
            Book.id != book_id
        ).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="ISBN already exists")
    
    # Update only provided fields
    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Delete a book"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.get("/books/isbn/{isbn}", response_model=BookResponse)
def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    """Get a book by ISBN"""
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

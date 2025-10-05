from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Article, User
from schemas import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from auth import get_current_active_user

router = APIRouter()

@router.post("/articles/", response_model=ArticleResponse, status_code=201)
def create_article(article: ArticleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Create a new article"""
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.get("/articles/", response_model=ArticleListResponse)
def get_articles(
    skip: int = Query(0, ge=0, description="Number of articles to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of articles to return"),
    search: Optional[str] = Query(None, description="Search in title, author, and content"),
    category: Optional[str] = Query(None, description="Filter by category"),
    published: Optional[str] = Query(None, description="Filter by publication status"),
    db: Session = Depends(get_db)
):
    """Get all articles with pagination, search, and filters"""
    query = db.query(Article)
    
    # Apply search filter
    if search:
        query = query.filter(
            (Article.title.contains(search)) | 
            (Article.author.contains(search)) |
            (Article.content.contains(search))
        )
    
    # Apply category filter
    if category:
        query = query.filter(Article.category == category)
    
    # Apply published status filter
    if published:
        query = query.filter(Article.published == published)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    articles = query.offset(skip).limit(limit).all()
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific article by ID"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/articles/{article_id}", response_model=ArticleResponse)
def update_article(article_id: int, article_update: ArticleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Update an article"""
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Update only provided fields
    update_data = article_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_article, field, value)
    
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Delete an article"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}

@router.get("/articles/category/{category}", response_model=ArticleListResponse)
def get_articles_by_category(
    category: str,
    skip: int = Query(0, ge=0, description="Number of articles to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of articles to return"),
    db: Session = Depends(get_db)
):
    """Get articles by category"""
    query = db.query(Article).filter(Article.category == category)
    
    total = query.count()
    articles = query.offset(skip).limit(limit).all()
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

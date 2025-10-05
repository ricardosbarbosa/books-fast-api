from .books import router as books_router
from .articles import router as articles_router
from .auth import router as auth_router

__all__ = ["books_router", "articles_router", "auth_router"]

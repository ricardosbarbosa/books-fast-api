from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import (
    UserCreate, UserResponse, Token, UserLogin, 
    GoogleUserInfo, GoogleAuthResponse
)
from auth import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user, 
    get_current_superuser,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from google_auth import (
    get_google_authorization_url, exchange_code_for_token, 
    get_google_user_info
)

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return access token"""
    user = authenticate_user(db, form_data.username, form_data.password)  # form_data.username is actually email now
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@router.get("/users", response_model=list[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get all users (superuser only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Get a specific user (superuser only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Google OAuth2 Routes

@router.get("/google/login")
async def google_login():
    """Initiate Google OAuth2 login"""
    try:
        authorization_url, state = get_google_authorization_url()
        return {"authorization_url": authorization_url, "state": state}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth2 callback"""
    try:
        # Get authorization code from query parameters
        code = request.query_params.get("code")
        error = request.query_params.get("error")
        
        if error:
            raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")
        
        if not code:
            raise HTTPException(status_code=400, detail="Authorization code not provided")
        
        print(f"Received authorization code: {code[:10]}...")
        
        # Exchange code for access token
        token_response = await exchange_code_for_token(code)
        print(f"Token response keys: {list(token_response.keys())}")
        
        access_token = token_response.get("access_token")
        
        if not access_token:
            print(f"Full token response: {token_response}")
            raise HTTPException(status_code=400, detail="Failed to get access token")
        
        # Get user info from Google
        print("Fetching user info from Google...")
        google_user_info = await get_google_user_info(access_token)
        print(f"Google user info: {google_user_info}")
        
        # Check if user already exists
        print("Checking for existing user...")
        existing_user = db.query(User).filter(
            (User.google_id == google_user_info["id"]) | 
            (User.email == google_user_info["email"])
        ).first()
        print(f"Existing user found: {existing_user is not None}")
        
        if existing_user:
            # Update existing user with Google info if needed
            if not existing_user.google_id:
                existing_user.google_id = google_user_info["id"]
                existing_user.provider = "google"
                existing_user.avatar_url = google_user_info.get("picture")
                db.commit()
                db.refresh(existing_user)
        else:
            # Create new user
            print("Creating new user...")
            try:
                new_user = User(
                    email=google_user_info["email"],
                    full_name=google_user_info["name"],
                    google_id=google_user_info["id"],
                    avatar_url=google_user_info.get("picture"),
                    provider="google",
                    is_active=True,
                    is_superuser=False
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                existing_user = new_user
                print(f"New user created with ID: {new_user.id}")
            except Exception as e:
                print(f"Error creating user: {str(e)}")
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
        
        # Create JWT token for our API
        jwt_token = create_access_token(
            data={"sub": existing_user.email}, 
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return GoogleAuthResponse(
            access_token=jwt_token,
            token_type="bearer",
            user=existing_user
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google authentication failed: {str(e)}")

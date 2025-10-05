"""
Google OAuth2 Authentication Configuration
"""

import os
from authlib.integrations.httpx_client import AsyncOAuth2Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google OAuth2 Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/google/callback")

# Google OAuth2 URLs
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# OAuth2 Scopes
GOOGLE_SCOPES = [
    "openid",
    "email", 
    "profile"
]

def get_google_oauth_client():
    """Create and return a Google OAuth2 client"""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("Google OAuth2 credentials not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.")
    
    return AsyncOAuth2Client(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=GOOGLE_REDIRECT_URI,
        scope=GOOGLE_SCOPES
    )

def get_google_authorization_url():
    """Generate Google OAuth2 authorization URL"""
    client = get_google_oauth_client()
    authorization_url, state = client.create_authorization_url(
        GOOGLE_AUTHORIZATION_URL,
        access_type="offline",
        include_granted_scopes="true"
    )
    return authorization_url, state

async def get_google_user_info(access_token: str):
    """Get user information from Google using access token"""
    try:
        import httpx
        print(f"Making request to Google API: {GOOGLE_USER_INFO_URL}")
        print(f"Using access token: {access_token[:20]}...")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GOOGLE_USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            print(f"Google API response status: {response.status_code}")
            response.raise_for_status()
            user_info = response.json()
            print(f"Google API response: {user_info}")
            return user_info
    except Exception as e:
        print(f"Error fetching user info from Google: {str(e)}")
        raise Exception(f"Failed to fetch user info from Google: {str(e)}")

async def exchange_code_for_token(code: str):
    """Exchange authorization code for access token"""
    try:
        client = get_google_oauth_client()
        token_response = await client.fetch_token(
            GOOGLE_TOKEN_URL,
            code=code
        )
        return token_response
    except Exception as e:
        print(f"Token exchange error: {str(e)}")
        raise Exception(f"Token exchange failed: {str(e)}")

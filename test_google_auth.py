#!/usr/bin/env python3
"""
Test script to verify Google OAuth2 configuration
"""

import asyncio
import os
from dotenv import load_dotenv
from google_auth import get_google_oauth_client, get_google_authorization_url

async def test_google_config():
    """Test Google OAuth2 configuration"""
    load_dotenv()
    
    print("🔍 Testing Google OAuth2 Configuration...")
    print("=" * 50)
    
    # Test 1: Check environment variables
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
    
    print(f"✅ Client ID: {client_id}")
    print(f"✅ Client Secret: {'SET' if client_secret else 'NOT SET'}")
    print(f"✅ Redirect URI: {redirect_uri}")
    
    # Test 2: Create OAuth client
    try:
        client = get_google_oauth_client()
        print("✅ OAuth client created successfully")
    except Exception as e:
        print(f"❌ Failed to create OAuth client: {e}")
        return
    
    # Test 3: Generate authorization URL
    try:
        auth_url, state = get_google_authorization_url()
        print(f"✅ Authorization URL generated")
        print(f"   State: {state}")
        print(f"   URL length: {len(auth_url)}")
    except Exception as e:
        print(f"❌ Failed to generate authorization URL: {e}")
        return
    
    print("\n🎯 Configuration looks good!")
    print("Next steps:")
    print("1. Copy the authorization URL from the API response")
    print("2. Open it in your browser")
    print("3. Complete the Google authentication")
    print("4. Check the server logs for debug information")

if __name__ == "__main__":
    asyncio.run(test_google_config())

#!/usr/bin/env python3
"""
Environment Setup Script
This script helps you set up your environment variables for the Books & Articles API.
"""

import os
import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Create a .env file from the template"""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ Setup cancelled.")
            return
    
    # Generate a secure secret key
    secret_key = generate_secret_key()
    
    # Read the template
    with open('env.example', 'r') as f:
        template = f.read()
    
    # Replace the placeholder secret key
    env_content = template.replace(
        'your-super-secret-key-change-this-in-production-123456789',
        secret_key
    )
    
    # Write the .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created successfully!")
    print(f"🔑 Generated secret key: {secret_key[:20]}...")
    print("📝 You can edit .env file to customize other settings.")

def main():
    print("🚀 Books & Articles API - Environment Setup")
    print("=" * 50)
    
    if not os.path.exists('env.example'):
        print("❌ env.example file not found!")
        return
    
    create_env_file()
    
    print("\n📋 Next steps:")
    print("1. Review and edit .env file if needed")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: python main.py")
    print("4. Access the API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()

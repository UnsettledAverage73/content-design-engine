import os
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
import httpx

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

class User(Dict[str, Any]):
    id: str

async def get_current_user(request: Request) -> User:
    """
    Validates the Supabase JWT from the Authorization header.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header.split(" ")[1]
    
    try:
        # Note: In production, you'd decode with the secret from Supabase
        # payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        
        # For this prototype, we'll implement a validation logic 
        # or use the secret if provided in .env
        if not SUPABASE_JWT_SECRET:
             # If secret isn't provided yet, we'll allow a mock mode for local dev
             # but raise an error in GTM plan for production
             if os.getenv("ENV") == "production":
                 raise HTTPException(status_code=500, detail="JWT Secret not configured")
             # Mock user for local testing without Supabase credentials
             return {"id": "mock-user-123"}

        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"id": user_id}
        
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

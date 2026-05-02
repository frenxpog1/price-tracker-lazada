"""
Vercel serverless function entry point for FastAPI backend.
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from app.main import app
    handler = app
except Exception as e:
    # If import fails, create a minimal FastAPI app to show the error
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    handler = FastAPI()
    
    @handler.get("/")
    @handler.get("/{path:path}")
    async def error_handler(path: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to initialize application",
                "details": str(e),
                "type": type(e).__name__
            }
        )

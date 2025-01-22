from fastapi import FastAPI
from typing import Dict
from app.api.config import add_cors_middleware
from app.api.routers import router as problems_router

app = FastAPI()

# Apply CORS middleware settings
add_cors_middleware(app)

# Add all sub routers to main router
app.include_router(problems_router)

@app.get('/')
async def home() -> Dict[str, str]:
    return {'message': 'Welcome to the CodeScript API'}

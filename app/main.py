import httpx
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from typing import Dict
from app.config import add_cors_middleware
from app.routers import router as problems_router
from app.schemas import LLMRequest, LLMResponse

load_dotenv()

LLM_API_URL = os.getenv('LLM_API_URL')

app = FastAPI()

# add_cors_middleware(app)

@app.get('/')
async def home() -> Dict[str, str]:
    return {'message': 'Welcome to the CodeScript API'}

@app.post('/generate_feedback', response_model=LLMResponse)
async def generate_feedback_route(request: LLMRequest) -> LLMResponse:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LLM_API_URL, json=request.model_dump())
            response.raise_for_status() 
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f'Error from LLM API: {e}')
        
app.include_router(problems_router)

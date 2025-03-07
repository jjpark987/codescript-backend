from fastapi import FastAPI, Depends
from typing import Dict
from app.config import add_cors_middleware, processing_limiter, request_lock
from app.llm import run_deepseek
from app.routers import router as problems_router
from app.schemas import LLMRequest, LLMResponse

app = FastAPI()
add_cors_middleware(app)

@app.get('/')
async def home() -> Dict[str, str]:
    return {'message': 'Welcome to the CodeScript API'}

@app.post('/generate_feedback', response_model=LLMResponse, dependencies=[Depends(processing_limiter)])
def generate_feedback_route(request: LLMRequest) -> LLMResponse:
    try:
        response = run_deepseek(request.problem_data, request.user_submission)
        return LLMResponse.model_validate(response)
    finally:
        request_lock.release()

app.include_router(problems_router)

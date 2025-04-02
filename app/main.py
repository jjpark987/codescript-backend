from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from os import path
from typing import Dict
from app.config import add_cors_middleware, processing_limiter, request_lock
from app.database import is_demo_mode
from app.llm import run_deepseek
from app.routers import router as problems_router
from app.schemas import LLMRequest, LLMResponse

app = FastAPI()
add_cors_middleware(app)

if not is_demo_mode():
    dist_path = path.join(path.dirname(__file__), 'static', 'dist')
    if path.exists(dist_path):
        app.mount('/', StaticFiles(directory=dist_path, html=True), name='static')

@app.get('/')
async def home() -> Dict[str, str]:
    return {'message': 'Welcome to the CodeScript API'}

@app.post('/generate_feedback', response_model=LLMResponse, dependencies=[Depends(processing_limiter)])
def generate_feedback_route(request: LLMRequest) -> LLMResponse:
    try:
        if is_demo_mode():
            demo_response = {
                'analysis': 'This version is only for demo purposes.',
                'suggestion': '',
                'score': 3
            }
            return LLMResponse.model_validate(demo_response)
        else:
            response = run_deepseek(request.problem_data, request.user_submission)
            return LLMResponse.model_validate(response)
    finally:
        request_lock.release()

app.include_router(problems_router)

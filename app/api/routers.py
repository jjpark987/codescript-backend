from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.schemas import ProblemCreate, ProblemResponse
from app.api.crud import post_problem  
from app.database.config import get_session

router = APIRouter()

@router.post('/problems', response_model=ProblemResponse, status_code=201)
async def post_problem_route(problem: ProblemCreate, db: Session = Depends(get_session)) -> ProblemResponse:
    return await post_problem(db, problem)  

from app.crud import post_problem, get_problem, get_random_problem
from app.database import get_session
from app.schemas import ProblemCreate, ProblemResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/problems', response_model=ProblemResponse)
async def post_problem_route(problem: ProblemCreate, db: Session = Depends(get_session)) -> ProblemResponse:
    return await post_problem(db, problem)

@router.get('/problems/random')
async def get_random_problem_route(db: Session = Depends(get_session)):
    return await get_random_problem(db)

@router.get('/problems/{problem_id}')
async def get_problem_route(problem_id: int, db: Session = Depends(get_session)):
    return await get_problem(db, problem_id)

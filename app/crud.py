from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models import Problem, Subcategory
from app.schemas import ProblemCreate, ProblemResponse

async def post_problem(db: Session, problem: ProblemCreate) -> ProblemResponse:
    result = await db.execute(select(Subcategory).filter(Subcategory.id == problem.subcategory_id))
    subcategory = result.scalar_one_or_none()

    if not subcategory: 
        raise HTTPException(status_code=404, detail=f'❌ CRUD: Subcategory {problem.subcategory_id} not found')
    
    result = await db.execute(select(Problem).filter(Problem.title == problem.title))
    existing_problem = result.scalar_one_or_none()

    if existing_problem:
        raise HTTPException(status_code=409, detail=f'⏭️ CRUD: "{problem.title}" already exists')

    try:
        new_problem = Problem(
            title=problem.title,
            difficulty=problem.difficulty,
            image_urls=problem.image_urls,
            description=problem.description,
            examples=problem.examples,
            constraints=problem.constraints,
            subcategory_id=problem.subcategory_id
        )

        db.add(new_problem)
        await db.commit()
        await db.refresh(new_problem)

        print(f'✅ CRUD successfully created a new problem: {new_problem.title}')
        return ProblemResponse.model_validate(new_problem)

    except SQLAlchemyError as e:
        await db.rollback()
        print(f'🚨 CRUD database error: {str(e)}')
        raise HTTPException(status_code=500, detail='❌ CRUD: Database error')

    except Exception as e:
        print(f'🚨 CRUD unexpected error: {str(e)}')
        raise HTTPException(status_code=500, detail='❌ CRUD: Internal Server Error')
    
async def get_random_problem(db: Session) -> ProblemResponse:
    result = await db.execute(select(Problem).order_by(func.random()).limit(1))
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail='❌ CRUD: Random problem not found')

    return ProblemResponse.model_validate(problem)

async def get_problem(db: Session, problem_id: int) -> ProblemResponse:
    result = await db.execute(select(Problem).filter(Problem.id == problem_id))
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail=f'❌ CRUD: Problem {problem_id} not found')

    return ProblemResponse.model_validate(problem)

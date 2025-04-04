from app.models import Problem, Subcategory
from app.util import get_signed_image_url
from app.schemas import ProblemCreate, ProblemResponse
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

async def post_problem(db: Session, problem: ProblemCreate) -> ProblemResponse:
    result = await db.execute(
        select(Subcategory, Problem)
        .outerjoin(Problem, Problem.title == problem.title)
        .filter(Subcategory.id == problem.subcategory_id)
    )

    subcategory, existing_problem = result.first() or (None, None)

    if not subcategory: 
        raise HTTPException(status_code=404, detail=f'❌ CRUD: Subcategory {problem.subcategory_id} not found')
    if existing_problem:
        raise HTTPException(status_code=409, detail=f'⏭️ CRUD: {problem.title} already exists')

    try:
        new_problem = Problem(
            subcategory_id=problem.subcategory_id,
            title=problem.title,
            difficulty=problem.difficulty,
            description=problem.description,
            constraints=problem.constraints,
            examples=problem.examples,
            image_paths=problem.image_paths
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
    
async def get_random_problem(db: Session) -> dict:
    result = await db.execute(select(Problem).order_by(func.random()).limit(1))
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail='❌ CRUD: Random problem not found')

    signed_urls = [get_signed_image_url(path) for path in problem.image_paths]

    return {
            'problem': ProblemResponse.model_validate(problem),
            'image_urls': signed_urls
        }

async def get_problem(db: Session, problem_id: int) -> dict:
    result = await db.execute(select(Problem).filter(Problem.id == problem_id))
    problem = result.scalar_one_or_none()

    if not problem:
        raise HTTPException(status_code=404, detail=f'❌ CRUD: Problem {problem_id} not found')

    signed_urls = [get_signed_image_url(path) for path in problem.image_paths]

    return {
            'problem': ProblemResponse.model_validate(problem),
            'image_urls': signed_urls
        }

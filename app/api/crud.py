from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.api.models import Problem, Subcategory
from app.api.schemas import ProblemCreate, ProblemResponse

async def post_problem(db: Session, problem: ProblemCreate) -> ProblemResponse:
    # Ensure subcategory exists
    result = await db.execute(select(Subcategory).filter(Subcategory.id == problem.subcategory_id))
    subcategory = result.scalar_one_or_none()
    if not subcategory:
        raise HTTPException(status_code=400, detail=f'Subcategory ID {problem.subcategory_id} not found.')

    # Check if the problem already exists (avoid duplicates)
    result = await db.execute(select(Problem).filter(Problem.title == problem.title))
    existing_problem = result.scalar_one_or_none()
    if existing_problem:
        raise HTTPException(status_code=400, detail=f'{problem.title} already exists.')

    # Create new Problem object
    new_problem = Problem(
        title=problem.title,
        difficulty=problem.difficulty,
        image_urls=problem.image_urls,
        description=problem.description,
        examples=problem.examples,
        constraints=problem.constraints,
        subcategory_id=problem.subcategory_id
    )

    # Insert into DB
    db.add(new_problem)
    await db.commit()
    await db.refresh(new_problem)

    return ProblemResponse.model_validate(new_problem)

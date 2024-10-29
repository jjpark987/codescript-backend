import asyncio
from sqlalchemy.future import select
from app.database.config import get_session_seed, engine
from app.api.models import Category

async def seed_categories():
    async with get_session_seed() as db:
        result = await db.execute(select(Category))
        existing_categories = result.scalars().all()
        if not existing_categories:
            categories_to_add = [
                Category(name="combinatorics"),
                Category(name="graphs"),
                Category(name="linked lists"),
                Category(name="manipulations"),
                Category(name="matrix"),
                Category(name="misc"),
                Category(name="optimizations"),
                Category(name="searching"),
                Category(name="sorting"),
                Category(name="trees")
            ]
            
            db.add_all(categories_to_add)
            await db.commit()
            print("Categories seeded successfully.")
        else:
            print("Categories already exist; seeding skipped.")

async def main():
    try:
        await seed_categories()
    finally:
        await engine.dispose()

if __name__ == '__main__':
    asyncio.run(main())

# Run from the root using `python -m app.database.seed`

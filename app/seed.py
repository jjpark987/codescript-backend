from asyncio import run
from sqlalchemy.future import select
from app.database import get_session_seed, engine
from app.models import Category, Subcategory

async def seed_categories() -> None:
    async with get_session_seed() as db:
        result = await db.execute(select(Category))
        existing_categories = {category.name for category in result.scalars()}
        
        categories_to_add = [
            {'name': 'data manipulations', 'description': 'Focuses on transforming, rearranging, or deriving results from data.'},
            {'name': 'combinatorics', 'description': 'Explores counting or generating combinations, permutations, and subsets.'},
            {'name': 'optimizations', 'description': 'Aims to find optimal solutions by maximizing or minimizing specific criteria.'}
        ]
        
        categories_to_insert = [
            Category(name=category['name'], description=category['description']) 
            for category in categories_to_add 
            if category['name'] not in existing_categories
        ]
        
        if categories_to_insert:
            db.add_all(categories_to_insert)
            try:
                await db.commit()
                print('Categories seeded successfully.')
            except Exception as e:
                await db.rollback()
                print(f'Error seeding categories: {e}')
        else:
            print('Categories already exist; seeding skipped.')

async def seed_subcategories() -> None:
    async with get_session_seed() as db:
        result = await db.execute(select(Subcategory))
        existing_subcategories = {subcategory.name for subcategory in result.scalars()}

        subcategories_to_add = [
            {'name': 'reformatting', 'description': 'Focuses on rearranging and transforming data.', 'category_name': 'data manipulations'},
            {'name': 'reducing', 'description': 'Involves summarizing or aggregating data.', 'category_name': 'data manipulations'},
            {'name': 'counting', 'description': 'Deals with counting elements or sets.', 'category_name': 'combinatorics'},
            {'name': 'generating', 'description': 'Focuses on creating combinations, permutations, or subsets.', 'category_name': 'combinatorics'},
            {'name': 'strings', 'description': 'Optimization problems focused on string manipulation.', 'category_name': 'optimizations'},
            {'name': 'arrays', 'description': 'Optimizing solutions for array-based problems.', 'category_name': 'optimizations'},
            {'name': 'structures', 'description': 'Optimization for graphs, trees, grids, or matrices.', 'category_name': 'optimizations'},
            {'name': 'heaps', 'description': 'Focuses on heap-based data structures.', 'category_name': 'optimizations'},
            {'name': 'processes', 'description': 'Optimizes processes like scheduling or workflows.', 'category_name': 'optimizations'},
        ]

        categories_result = await db.execute(select(Category))
        categories = {category.name: category for category in categories_result.scalars()}

        subcategories_to_insert = [
            Subcategory(
                name=subcategory['name'],
                description=subcategory['description'],
                category_id=categories[subcategory['category_name']].id
            )
            for subcategory in subcategories_to_add
            if subcategory['name'] not in existing_subcategories
        ]

        if subcategories_to_insert:
            db.add_all(subcategories_to_insert)
            try:
                await db.commit()
                print('Subcategories seeded successfully.')
            except Exception as e:
                await db.rollback()
                print(f'Error seeding subcategories: {e}')
        else:
            print('Subcategories already exist; seeding skipped.')

async def main():
    try:
        await seed_categories()
        await seed_subcategories()
    finally:
        await engine.dispose()

if __name__ == '__main__':
    run(main())
    
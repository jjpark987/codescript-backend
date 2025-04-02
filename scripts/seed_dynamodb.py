from asyncio import run
from boto3 import resource
from dotenv import load_dotenv
from sqlalchemy import select
from app.database import get_session_seed, engine
from app.models import Problem

load_dotenv('.env.demo')
dynamodb = resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('codescript-problems')

async def seed_dynamodb():
    async with get_session_seed() as session:
        result = await session.execute(select(Problem))
        problems = result.scalars().all()

        with table.batch_writer() as batch:
            for problem in problems:
                item = {
                    'id': problem.id, 
                    'title': problem.title,
                    'difficulty': problem.difficulty,
                    'description': problem.description,
                    'constraints': problem.constraints,  
                    'examples': problem.examples,        
                    'image_paths': problem.image_paths,  
                    'subcategory_id': problem.subcategory_id,
                }
                batch.put_item(Item=item)

    print('Data migration complete.')

async def main():
    try:
        await seed_dynamodb()
    finally:
        await engine.dispose()

if __name__ == '__main__':
    run(main())

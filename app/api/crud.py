# from pydantic import BaseModel
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.orm.exc import NoResultFound
# from typing import Type, TypeVar, List

# ModelType = TypeVar('ModelType')
# SchemaType = TypeVar('SchemaType', bound=BaseModel)

# class CRUD:
#     def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
#         self.model = model
#         self.schema = schema

#     async def create(self, db: AsyncSession, obj_in: SchemaType) -> ModelType:
#         try:
#             obj_data = obj_in.model_dump()
#             obj = self.model(**obj_data)
#             db.add(obj)
#             await db.commit()
#             await db.refresh(obj)
#             return obj
#         except Exception as e:
#             print(f'Error creating {self.model.__name__}: {e}')
#             raise

#     async def get(self, db: AsyncSession, id: int) -> ModelType:
#         try:
#             obj = await db.get(self.model, id)
#             if obj is None:
#                 raise NoResultFound(f'{self.model.__name__} with id {id} not found.')
#             return obj
#         except NoResultFound as e:
#             print(e)
#             raise
#         except Exception as e:
#             print(f'Error retrieving {self.model.__name__} with id {id}: {e}')
#             raise

#     async def get_all(self, db: AsyncSession) -> List[ModelType]:
#         try:
#             result = await db.execute(select(self.model))
#             return result.scalars().all()
#         except Exception as e:
#             print(f'Error retrieving all {self.model.__name__} entries: {e}')
#             raise

#     async def update(self, db: AsyncSession, id: int, obj_in: SchemaType) -> ModelType:
#         try:
#             obj = await self.get(db, id)
#             obj_data = obj_in.model_dump()
#             for key, value in obj_data.items():
#                 setattr(obj, key, value)
#             await db.commit()
#             await db.refresh(obj)
#             return obj
#         except NoResultFound as e:
#             print(f'{self.model.__name__} with id {id} not found: {e}')
#             raise
#         except Exception as e:
#             print(f'Error updating {self.model.__name__} with id {id}: {e}')
#             raise

#     async def delete(self, db: AsyncSession, id: int) -> None:
#         try:
#             obj = await self.get(db, id)
#             await db.delete(obj)
#             await db.commit()
#         except NoResultFound as e:
#             print(f'{self.model.__name__} with id {id} not found: {e}')
#             raise
#         except Exception as e:
#             print(f'Error deleting {self.model.__name__} with id {id}: {e}')
#             raise

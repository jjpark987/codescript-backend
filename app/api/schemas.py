# from datetime import datetime
# from pydantic import BaseModel
# from typing import Optional, List, Dict

# class BaseConfigModel(BaseModel):
#     class Config:
#         from_attributes = True

# class CategoryRead(BaseConfigModel):
#     name: str
#     description: Optional[str]

# class SubcategoryRead(CategoryRead):
#     pass

# class ProblemRead(BaseConfigModel):
#     title: str
#     difficulty: int
#     description: str
#     example: List[Dict[str, str]]
#     constraints: str

# class SubmissionRead(BaseConfigModel):
#     content: str
#     created_at: datetime
#     updated_at: datetime

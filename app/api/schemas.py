from pydantic import BaseModel, Field
from typing import List, Dict

class ProblemCreate(BaseModel):
    subcategory_id: int
    title: str
    difficulty: int = Field(..., ge=1, le=3)
    image_urls: List[str]
    description: str
    examples: List[Dict[str, str]]
    constraints: str

    class Config:
        from_attributes = True

class ProblemResponse(ProblemCreate):
    id: int

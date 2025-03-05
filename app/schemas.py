from pydantic import BaseModel, Field
from typing import List, Dict

class ProblemCreate(BaseModel):
    subcategory_id: int
    title: str
    difficulty: int = Field(..., ge=1, le=3)
    image_urls: List[str]
    description: str
    examples: List[Dict[str, str]]
    constraints: List[str]

    class Config:
        from_attributes = True

class ProblemResponse(ProblemCreate):
    id: int

class LLMRequest(BaseModel):
    problem_data: dict
    user_submission: str

class LLMResponse(BaseModel):
    analysis: str
    suggestions: List[str]
    score: int = Field(..., ge=0, le=3)

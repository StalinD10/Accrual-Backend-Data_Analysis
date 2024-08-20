from pydantic import BaseModel
from typing import Optional
class CategoryDocentFaculty(BaseModel):
    category: str
    names: Optional[str] = None
    lastNames: Optional[str] = None
    faculty: Optional[str] = None
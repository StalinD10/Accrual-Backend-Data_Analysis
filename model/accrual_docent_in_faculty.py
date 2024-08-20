from typing import Optional
from pydantic import BaseModel

class AccrualDocentInFaculty(BaseModel):
    names: Optional[str] = None
    lastNames: Optional[str] = None
    faculty: Optional[str] = None
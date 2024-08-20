from typing import Optional
from pydantic import BaseModel

class CountryDocentsFaculty(BaseModel):
    country: str
    names: Optional[str] = None
    lastNames: Optional[str] = None
    faculty: Optional[str] = None

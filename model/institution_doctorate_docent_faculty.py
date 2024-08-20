from typing import Optional
from pydantic import BaseModel

class InstitutionDoctorateDocentFaculty(BaseModel):
    institution: str
    names: Optional[str] = None
    lastNames: Optional[str] = None
    faculty: Optional[str] = None
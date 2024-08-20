from typing import Optional

from pydantic import BaseModel

class Modality_Accrual_Docent(BaseModel):
    modality: str
    names: Optional[str] = None
    lastNames: Optional[str] = None
    faculty: Optional[str] = None

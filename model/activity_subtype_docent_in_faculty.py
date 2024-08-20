from pydantic import BaseModel

class ActivitySubtypeDocent(BaseModel):
    names: str
    lastNames: str
    subtype: str
    faculty: str

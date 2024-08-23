from pydantic import BaseModel

class ActivityTypeDocent(BaseModel):
    names: str
    lastNames: str
    typeActivity: str
    faculty: str
    period: str

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    baseline_wpm: int
    baseline_comprehension: int
    baseline_memory: int

    class Config:
        from_attributes = True

class BaselineIn(BaseModel):
    baseline_wpm: int = Field(ge=0, le=2000)
    baseline_comprehension: int = Field(ge=0, le=100)
    baseline_memory: int = Field(ge=0, le=50)

class ChangePasswordIn(BaseModel):
    current_password: str = Field(min_length=6, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)
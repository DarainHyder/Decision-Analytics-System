from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# User
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Option
class OptionBase(BaseModel):
    option_name: str
    reasoning: Optional[str] = None

class OptionCreate(OptionBase):
    pass

class Option(OptionBase):
    id: int
    decision_id: int
    
    class Config:
        from_attributes = True

# Assumption
class AssumptionBase(BaseModel):
    assumption_text: str
    status: Optional[str] = "pending"

class AssumptionCreate(AssumptionBase):
    pass

class AssumptionUpdate(BaseModel):
    status: str

class Assumption(AssumptionBase):
    id: int
    decision_id: int
    
    class Config:
        from_attributes = True

# Review
class ReviewBase(BaseModel):
    outcome_rating: int
    outcome_notes: Optional[str] = None
    lessons_learned: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    decision_id: int
    reviewed_at: datetime
    
    class Config:
        from_attributes = True

# Decision
class DecisionBase(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    confidence_score: int
    expected_outcome: Optional[str] = None
    decision_date: Optional[datetime] = None
    review_date: Optional[datetime] = None

class DecisionCreate(DecisionBase):
    options: List[OptionCreate] = []
    assumptions: List[AssumptionCreate] = []

class Decision(DecisionBase):
    id: int
    user_id: int
    created_at: datetime
    decision_quality: Optional[str] = None
    outcome_quality: Optional[str] = None
    
    options: List[Option] = []
    assumptions: List[Assumption] = []
    review: Optional[Review] = None
    
    class Config:
        from_attributes = True

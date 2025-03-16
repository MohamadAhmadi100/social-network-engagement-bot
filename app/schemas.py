from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class ProfileBase(BaseModel):
    username: str = Field(..., example="instagram_user")
    instagram_user_id: str = Field(..., example="17841400000000")


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    instagram_user_id: Optional[str] = None


class ProfileOut(ProfileBase):
    id: int
    current_follower_count: int
    last_checked: datetime

    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    milestone: int = Field(..., example=1000)

    @validator('milestone')
    def milestone_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Milestone must be positive')
        return v


class AlertCreate(AlertBase):
    profile_id: int


class AlertOut(AlertBase):
    id: int
    profile_id: int
    notified: int

    class Config:
        from_attributes = True


class FollowerHistoryOut(BaseModel):
    id: int
    count: int
    timestamp: datetime

    class Config:
        from_attributes = True

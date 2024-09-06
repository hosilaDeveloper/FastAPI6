from datetime import date

from pydantic import BaseModel
from typing import List, Optional


class ExperienceBase(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str


class ExperienceCreate(ExperienceBase):
    pass


class Experience(ExperienceBase):
    id: int

    class Config:
        orm_mode = True


class EducationBase(BaseModel):
    title: str
    institution: str
    degree: str
    start_date: str
    end_date: str


class EducationCreate(EducationBase):
    pass


class Education(EducationBase):
    id: int

    class Config:
        orm_mode = True


class AboutBase(BaseModel):
    name: str
    bio: Optional[str]


class AboutCreate(AboutBase):
    experience_id: int
    education_id: int


class About(AboutBase):
    id: int
    experiences: List[Experience] = []
    educations: List[Education] = []

    class Config:
        orm_mode = True

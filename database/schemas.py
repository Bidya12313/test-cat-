from pydantic import BaseModel
from typing import List, Optional


class CatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float

class CatCreate(CatBase):
    pass

class Cat(CatBase):
    id: int
    status: str

    class Config:
        orm_mode = True


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    complete: bool = False

class TargetCreate(TargetBase):
    pass

class Target(TargetBase):
    id: int

    class Config:
        orm_mode = True


class MissionBase(BaseModel):
    name: str
    complete: bool = False

class MissionCreate(MissionBase):
    targets: List[TargetCreate]

class Mission(MissionBase):
    id: int
    targets: List[Target] = []

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import List

class Observation(BaseModel):
    incident: str

class Action(BaseModel):
    type: str
    severity: str
    actions: List[str]

class Reward(BaseModel):
    score: float
from typing import List
from pydantic import BaseModel

class APIOutput(BaseModel):
    time_elapsed: str
    boxes: List
    scores: List
    classes: List
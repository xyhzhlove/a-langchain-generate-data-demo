from pydantic import BaseModel, Field
from typing import List, Dict


class PromptMeta(BaseModel):
    role_name: str
    task_name: str
    task_description: str
    input_data: Dict
    demostration: List


class ResultMeta(BaseModel):
    content: str
    scenic: str
    weather: str
    transport: str
    behavior: str

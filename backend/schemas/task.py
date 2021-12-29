from typing import List, Dict
from pydantic import BaseModel


class TaskComparison(BaseModel):
    count: int = 10
    delay: int = 1
    method_list: List = ["ray", "default", "celery"]


class MultipleRequest(BaseModel):
    address: str = "localhost"
    port: int = 8000
    endpoint: str = "background_task"
    delay: str = "1"
    timeout: int = 10


class Id(BaseModel):
    id: str


class TaskResult(BaseModel):
    id: str
    state: str
    result: Dict

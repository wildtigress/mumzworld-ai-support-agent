from pydantic import BaseModel
from typing import Dict


class Reply(BaseModel):
    en: str
    ar: str


class OutputSchema(BaseModel):
    intent: str
    reasoning: str
    reply: Reply
    requires_human: bool
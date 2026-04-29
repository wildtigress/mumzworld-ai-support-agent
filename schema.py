from pydantic import BaseModel

class OutputSchema(BaseModel):
    intent: str
    urgency: str
    confidence: float
    language: str
    reasoning: str
    reply: dict
    requires_human: bool
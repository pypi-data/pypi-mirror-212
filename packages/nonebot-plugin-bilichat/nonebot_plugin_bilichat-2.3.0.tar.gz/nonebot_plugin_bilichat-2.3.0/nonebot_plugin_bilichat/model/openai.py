from typing import Optional

from pydantic import BaseModel


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAI(BaseModel):
    error: bool = False
    message: str = ""
    response: str = ""
    token_usage: Optional[TokenUsage] = None
    raw: dict = {}

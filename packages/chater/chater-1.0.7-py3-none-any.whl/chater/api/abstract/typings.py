from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AuthTokenResponse(BaseModel):
    scope: str
    expires_in: datetime
    token_type: str
    access_token: str


class Plan(BaseModel):
    id: str
    title: str


class SubscriptionResponse(BaseModel):
    plan: Plan
    object: str
    account_name: str
    soft_limit_usd: float
    hard_limit_usd: float
    system_hard_limit_usd: float
    has_payment_method: bool
    access_until: datetime


class Message(BaseModel):
    role: Optional[str]
    content: Optional[str]


class Choice(BaseModel):
    index: int
    delta: Message
    finish_reason: Optional[str]


class StreamCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]

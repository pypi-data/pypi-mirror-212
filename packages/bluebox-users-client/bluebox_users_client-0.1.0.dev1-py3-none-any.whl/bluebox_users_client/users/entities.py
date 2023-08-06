import uuid
from dataclasses import dataclass


@dataclass
class User:
    user_id: uuid.UUID
    email: str
    balance: int

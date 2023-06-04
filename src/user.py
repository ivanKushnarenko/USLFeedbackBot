from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    id: int
    username: Optional[str]
    full_name: str
    description: str

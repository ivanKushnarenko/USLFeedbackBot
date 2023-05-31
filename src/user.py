from dataclasses import dataclass


@dataclass(frozen=True)
class UserInfo:
    username: str
    full_name: str
    description: str

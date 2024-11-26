from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    uid: str
    email: Optional[str] = None
    display_name: Optional[str] = None

@dataclass
class TokenVerification:
    id_token: str
    user: Optional[User] = None

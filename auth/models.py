from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    username: str
    password_hash: Optional[str]  # None for OAuth users
    auth_provider: str  # 'email', 'google'
    created_at: datetime
    last_login: Optional[datetime]

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        last_login = data.get('last_login')
        if isinstance(last_login, str) and last_login:
            last_login = datetime.fromisoformat(last_login)

        return cls(
            id=data.get('id', 0),
            email=data.get('email', ''),
            username=data.get('username', ''),
            password_hash=data.get('password_hash'),
            auth_provider=data.get('auth_provider', 'email'),
            created_at=created_at or datetime.now(),
            last_login=last_login
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
            'auth_provider': self.auth_provider,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

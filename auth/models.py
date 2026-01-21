from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class User:
    id: int
    email: str
    username: str
    password_hash: Optional[str]  # None for OAuth users
    auth_provider: str  # 'email', 'google'
    created_at: datetime
    last_login: Optional[datetime]
    nickname: Optional[str] = None
    phone: Optional[str] = None
    show_in_leaderboard: bool = False
    experience: int = 0
    credly_url: Optional[str] = None

    @property
    def display_name(self) -> str:
        """Return nickname if set, otherwise username."""
        return self.nickname if self.nickname else self.username

    @property
    def level(self) -> int:
        """Calculate level based on experience (100 XP per level)."""
        return self.experience // 100 + 1

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        last_login = data.get('last_login')
        if isinstance(last_login, str) and last_login:
            last_login = datetime.fromisoformat(last_login)

        # Handle show_in_leaderboard - SQLite stores as 0/1
        show_in_leaderboard = data.get('show_in_leaderboard', False)
        if isinstance(show_in_leaderboard, int):
            show_in_leaderboard = bool(show_in_leaderboard)

        return cls(
            id=data.get('id', 0),
            email=data.get('email', ''),
            username=data.get('username', ''),
            password_hash=data.get('password_hash'),
            auth_provider=data.get('auth_provider', 'email'),
            created_at=created_at or datetime.now(),
            last_login=last_login,
            nickname=data.get('nickname'),
            phone=data.get('phone'),
            show_in_leaderboard=show_in_leaderboard,
            experience=data.get('experience', 0) or 0,
            credly_url=data.get('credly_url')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
            'auth_provider': self.auth_provider,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'nickname': self.nickname,
            'phone': self.phone,
            'show_in_leaderboard': self.show_in_leaderboard,
            'experience': self.experience,
            'credly_url': self.credly_url
        }


@dataclass
class Certification:
    id: int
    user_id: int
    name: str
    code: str  # e.g., SAA-C03, CLF-C02
    issued_date: Optional[datetime]
    expiry_date: Optional[datetime]
    credential_id: Optional[str]
    credly_badge_url: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Certification':
        issued_date = data.get('issued_date')
        if isinstance(issued_date, str) and issued_date:
            issued_date = datetime.fromisoformat(issued_date)

        expiry_date = data.get('expiry_date')
        if isinstance(expiry_date, str) and expiry_date:
            expiry_date = datetime.fromisoformat(expiry_date)

        return cls(
            id=data.get('id', 0),
            user_id=data.get('user_id', 0),
            name=data.get('name', ''),
            code=data.get('code', ''),
            issued_date=issued_date,
            expiry_date=expiry_date,
            credential_id=data.get('credential_id'),
            credly_badge_url=data.get('credly_badge_url')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'code': self.code,
            'issued_date': self.issued_date.isoformat() if self.issued_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'credential_id': self.credential_id,
            'credly_badge_url': self.credly_badge_url
        }


# Available AWS Certifications for badges
AWS_CERTIFICATIONS = {
    "CLF-C02": "AWS Certified Cloud Practitioner",
    "SAA-C03": "AWS Certified Solutions Architect - Associate",
    "SOA-C02": "AWS Certified SysOps Administrator - Associate",
    "DVA-C02": "AWS Certified Developer - Associate",
    "SAP-C02": "AWS Certified Solutions Architect - Professional",
    "DOP-C02": "AWS Certified DevOps Engineer - Professional",
    "ANS-C01": "AWS Certified Advanced Networking - Specialty",
    "SCS-C02": "AWS Certified Security - Specialty",
    "MLS-C01": "AWS Certified Machine Learning - Specialty",
    "DBS-C01": "AWS Certified Database - Specialty",
    "PAS-C01": "AWS Certified Data Analytics - Specialty",
    "AIF-C01": "AWS Certified AI Practitioner"
}

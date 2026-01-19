from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import json


@dataclass
class Question:
    id: int
    exam_type: str
    domain: str
    difficulty: int
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: str
    reference: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        options = data.get('options', [])
        if isinstance(options, str):
            options = json.loads(options)
        return cls(
            id=data.get('id', 0),
            exam_type=data.get('exam_type', ''),
            domain=data.get('domain', ''),
            difficulty=data.get('difficulty', 1),
            question_text=data.get('question_text', ''),
            options=options,
            correct_answer=data.get('correct_answer', ''),
            explanation=data.get('explanation', ''),
            reference=data.get('reference', '')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'exam_type': self.exam_type,
            'domain': self.domain,
            'difficulty': self.difficulty,
            'question_text': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'reference': self.reference
        }


@dataclass
class ExamSession:
    id: int
    exam_type: str
    date: datetime
    score: int
    total: int
    time_spent: int
    weak_domains: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'ExamSession':
        weak_domains = data.get('weak_domains', [])
        if isinstance(weak_domains, str):
            weak_domains = json.loads(weak_domains)
        date = data.get('date')
        if isinstance(date, str):
            date = datetime.fromisoformat(date)
        return cls(
            id=data.get('id', 0),
            exam_type=data.get('exam_type', ''),
            date=date or datetime.now(),
            score=data.get('score', 0),
            total=data.get('total', 0),
            time_spent=data.get('time_spent', 0),
            weak_domains=weak_domains
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'exam_type': self.exam_type,
            'date': self.date.isoformat() if self.date else None,
            'score': self.score,
            'total': self.total,
            'time_spent': self.time_spent,
            'weak_domains': self.weak_domains
        }

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.score / self.total) * 100


DOMAINS = {
    "1": "Design Secure Architectures",
    "2": "Design Resilient Architectures",
    "3": "Design High-Performing Architectures",
    "4": "Design Cost-Optimized Architectures"
}

DOMAIN_WEIGHTS = {
    "1": 30,
    "2": 26,
    "3": 24,
    "4": 20
}

EXAM_CONFIG = {
    "SAA-C03": {
        "name": "AWS Solutions Architect Associate",
        "total_questions": 65,
        "scored_questions": 50,
        "time_minutes": 130,
        "passing_score": 720,
        "passing_percentage": 72
    }
}

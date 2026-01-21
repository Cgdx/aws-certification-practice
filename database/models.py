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
    correct_answer: str  # For single answer or comma-separated for multiple (e.g., "A,E")
    explanation: str
    reference: str
    question_id: str = ""  # Unique identifier like "SAA-C03-001"
    num_correct: int = 1  # Number of correct answers required

    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        options = data.get('options', [])
        if isinstance(options, str):
            options = json.loads(options)

        # Handle correct_answer - can be string or list
        correct_answer = data.get('correct_answer', '')
        if isinstance(correct_answer, list):
            correct_answer = ','.join(correct_answer)

        # Determine num_correct from correct_answer
        num_correct = data.get('num_correct', 1)
        if ',' in str(correct_answer):
            num_correct = len(correct_answer.split(','))

        return cls(
            id=data.get('id', 0),
            exam_type=data.get('exam_type', ''),
            domain=data.get('domain', ''),
            difficulty=data.get('difficulty', 1),
            question_text=data.get('question_text', ''),
            options=options,
            correct_answer=correct_answer,
            explanation=data.get('explanation', ''),
            reference=data.get('reference', ''),
            question_id=data.get('question_id', ''),
            num_correct=num_correct
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
            'reference': self.reference,
            'question_id': self.question_id,
            'num_correct': self.num_correct
        }

    @property
    def correct_answers_list(self) -> List[str]:
        """Return correct answers as a list."""
        if not self.correct_answer:
            return []
        return [a.strip() for a in self.correct_answer.split(',')]

    @property
    def is_multiple_choice(self) -> bool:
        """Check if question requires multiple answers."""
        return self.num_correct > 1


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

# Domain information per exam type
EXAM_DOMAINS = {
    "SAA-C03": {
        "1": {"name": "Design Secure Architectures", "weight": 30},
        "2": {"name": "Design Resilient Architectures", "weight": 26},
        "3": {"name": "Design High-Performing Architectures", "weight": 24},
        "4": {"name": "Design Cost-Optimized Architectures", "weight": 20}
    },
    "CLF-C02": {
        "1": {"name": "Cloud Concepts", "weight": 24},
        "2": {"name": "Security and Compliance", "weight": 30},
        "3": {"name": "Cloud Technology and Services", "weight": 34},
        "4": {"name": "Billing, Pricing, and Support", "weight": 12}
    },
    "AIF-C01": {
        "1": {"name": "Fundamentals of AI and ML", "weight": 20},
        "2": {"name": "Fundamentals of Generative AI", "weight": 24},
        "3": {"name": "Applications of Foundation Models", "weight": 28},
        "4": {"name": "Guidelines for Responsible AI", "weight": 14},
        "5": {"name": "Security, Compliance, and Governance for AI Solutions", "weight": 14}
    }
}

EXAM_CONFIG = {
    "SAA-C03": {
        "name": "AWS Solutions Architect Associate",
        "total_questions": 65,
        "scored_questions": 50,
        "time_minutes": 130,
        "passing_score": 720,
        "passing_percentage": 72,
        "available": True
    },
    "CLF-C02": {
        "name": "AWS Cloud Practitioner",
        "total_questions": 65,
        "scored_questions": 50,
        "time_minutes": 90,
        "passing_score": 700,
        "passing_percentage": 70,
        "available": False
    },
    "AIF-C01": {
        "name": "AWS AI Practitioner",
        "total_questions": 85,
        "scored_questions": 65,
        "time_minutes": 120,
        "passing_score": 700,
        "passing_percentage": 70,
        "available": False
    }
}

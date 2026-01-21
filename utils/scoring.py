from typing import Dict, List, Tuple, Set
from database.models import Question, DOMAINS, DOMAIN_WEIGHTS


def normalize_answer(answer: str) -> Set[str]:
    """Normalize answer string to a set of uppercase letters."""
    if not answer:
        return set()
    return set(a.strip().upper() for a in answer.split(',') if a.strip())


def is_answer_correct(user_answer: str, correct_answer: str) -> bool:
    """Check if user answer matches correct answer (supports multiple answers)."""
    user_set = normalize_answer(user_answer)
    correct_set = normalize_answer(correct_answer)
    return user_set == correct_set


def calculate_score(questions: List[Question], answers: Dict[int, str]) -> Tuple[int, int]:
    """
    Calculate the total score. Supports single and multiple answer questions.
    Only counts questions that were answered.

    Returns:
        Tuple of (correct_count, answered_questions)
    """
    correct = 0
    answered = 0
    for question in questions:
        user_answer = answers.get(question.id, '')
        if user_answer:  # Only count answered questions
            answered += 1
            if is_answer_correct(user_answer, question.correct_answer):
                correct += 1
    return correct, answered


def calculate_domain_scores(questions: List[Question],
                            answers: Dict[int, str]) -> Dict[str, Tuple[int, int]]:
    """
    Calculate scores by domain. Supports single and multiple answer questions.
    Only counts questions that were answered.

    Returns:
        Dictionary mapping domain_id to (correct_count, answered_in_domain)
    """
    domain_scores = {}

    for domain_id in DOMAINS.keys():
        domain_scores[domain_id] = [0, 0]

    for question in questions:
        user_answer = answers.get(question.id, '')
        if not user_answer:  # Skip unanswered questions
            continue

        domain_id = question.domain
        if domain_id not in domain_scores:
            domain_scores[domain_id] = [0, 0]

        domain_scores[domain_id][1] += 1

        if is_answer_correct(user_answer, question.correct_answer):
            domain_scores[domain_id][0] += 1

    return {k: tuple(v) for k, v in domain_scores.items()}


def identify_weak_domains(domain_scores: Dict[str, Tuple[int, int]],
                          threshold: float = 72.0) -> List[str]:
    """
    Identify domains where performance is below the threshold.

    Args:
        domain_scores: Dictionary of domain scores
        threshold: Minimum percentage considered passing

    Returns:
        List of domain IDs that are below threshold
    """
    weak_domains = []

    for domain_id, (correct, total) in domain_scores.items():
        if total > 0:
            percentage = (correct / total) * 100
            if percentage < threshold:
                weak_domains.append(domain_id)

    return sorted(weak_domains)


def calculate_weighted_score(domain_scores: Dict[str, Tuple[int, int]]) -> float:
    """
    Calculate a weighted score based on domain weights.

    Returns:
        Weighted percentage score
    """
    total_weight = 0
    weighted_sum = 0

    for domain_id, (correct, total) in domain_scores.items():
        if total > 0:
            weight = DOMAIN_WEIGHTS.get(domain_id, 0)
            percentage = (correct / total) * 100
            weighted_sum += percentage * weight
            total_weight += weight

    if total_weight == 0:
        return 0.0

    return weighted_sum / total_weight


def get_difficulty_distribution(questions: List[Question]) -> Dict[int, int]:
    """
    Get the distribution of questions by difficulty.

    Returns:
        Dictionary mapping difficulty level to count
    """
    distribution = {1: 0, 2: 0, 3: 0}

    for question in questions:
        if question.difficulty in distribution:
            distribution[question.difficulty] += 1

    return distribution


def calculate_scaled_score(correct: int, total: int, max_score: int = 1000) -> int:
    """
    Calculate a scaled score similar to AWS certification scoring.

    Args:
        correct: Number of correct answers
        total: Total number of questions
        max_score: Maximum possible score (default 1000)

    Returns:
        Scaled score between 100 and max_score
    """
    if total == 0:
        return 100

    percentage = correct / total
    scaled = 100 + (percentage * (max_score - 100))

    return int(scaled)

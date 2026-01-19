"""
Script to import quiz questions from HTML files into the database.
"""
import os
import re
import json
import html
from database.db_manager import DatabaseManager
from database.models import Question

# Mapping quiz titles to domains
DOMAIN_MAPPING = {
    # Domain 1: Design Secure Architectures (30%)
    "iam": "1",
    "security": "1",
    "encryption": "1",
    "cli": "1",

    # Domain 2: Design Resilient Architectures (26%)
    "high availability": "2",
    "scalability": "2",
    "disaster recovery": "2",
    "migration": "2",
    "rds": "2",
    "aurora": "2",
    "elasticache": "2",
    "route 53": "2",

    # Domain 3: Design High-Performing Architectures (24%)
    "ec2": "3",
    "s3": "3",
    "cloudfront": "3",
    "storage": "3",
    "databases": "3",
    "containers": "3",
    "serverless": "3",
    "lambda": "3",
    "messaging": "3",
    "integration": "3",
    "data management": "3",
    "global accelerator": "3",

    # Domain 4: Design Cost-Optimized Architectures (20%)
    "solutions architecture": "4",
    "whitepaper": "4",
    "architectures": "4",

    # Analytics & ML - Domain 3
    "analytics": "3",
    "machine learning": "3",

    # Monitoring - Domain 2
    "monitoring": "2",
    "auditing": "2",

    # VPC - Domain 1
    "vpc": "1",

    # Other services - Mixed
    "other services": "3",
}


def get_domain_from_title(title: str) -> str:
    """Determine domain based on quiz title."""
    title_lower = title.lower()

    for keyword, domain in DOMAIN_MAPPING.items():
        if keyword in title_lower:
            return domain

    # Default to domain 3 (High-Performing) for practice tests
    if "practice test" in title_lower:
        return "3"

    return "2"  # Default domain


def get_difficulty_from_title(title: str) -> int:
    """Determine difficulty based on quiz title."""
    title_lower = title.lower()

    # Practice tests are harder
    if "practice test" in title_lower:
        return 3

    # SAA Level quizzes are medium-hard
    if "saa level" in title_lower:
        return 2

    # Advanced quizzes are harder
    if "advanced" in title_lower:
        return 3

    # Fundamentals are easier
    if "fundamental" in title_lower:
        return 1

    # Default to medium
    return 2


def clean_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    if not text:
        return ""

    # Decode HTML entities
    text = html.unescape(text)

    # Remove HTML tags but keep content
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up whitespace
    text = ' '.join(text.split())

    return text.strip()


def extract_quiz_data(html_content: str) -> dict:
    """Extract quizData JSON from HTML file."""
    # Look for the quizData assignment
    pattern = r'const quizData = ({.*?});'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        return None

    json_str = match.group(1)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return None


def parse_questions(quiz_data: dict, source_file: str) -> list:
    """Parse questions from quiz data."""
    questions = []

    quiz_title = quiz_data.get('quiz_title', 'Unknown Quiz')
    domain = get_domain_from_title(quiz_title)
    difficulty = get_difficulty_from_title(quiz_title)

    for q in quiz_data.get('questions', []):
        prompt = q.get('prompt', {})

        # Get question text
        question_text = clean_html(prompt.get('question', ''))
        if not question_text:
            continue

        # Get answers
        raw_answers = prompt.get('answers', [])
        options = []
        for i, ans in enumerate(raw_answers):
            letter = chr(65 + i)  # A, B, C, D...
            clean_ans = clean_html(ans)
            options.append(f"{letter}. {clean_ans}")

        if not options:
            continue

        # Get correct answer
        correct_responses = q.get('correct_response', [])
        if correct_responses:
            correct_answer = correct_responses[0].upper()
        else:
            continue

        # Get explanation
        explanation = ""
        feedbacks = prompt.get('feedbacks', [])

        # Try to get the explanation for the correct answer
        if feedbacks:
            correct_idx = ord(correct_answer) - ord('A')
            if correct_idx < len(feedbacks) and feedbacks[correct_idx]:
                explanation = clean_html(feedbacks[correct_idx])

        # Also check for general explanation
        if not explanation and prompt.get('explanation'):
            explanation = clean_html(prompt.get('explanation'))

        # If still no explanation, combine all feedbacks
        if not explanation and feedbacks:
            all_feedbacks = [clean_html(f) for f in feedbacks if f]
            if all_feedbacks:
                explanation = " | ".join(all_feedbacks)

        question = Question(
            id=0,
            exam_type="SAA-C03",
            domain=domain,
            difficulty=difficulty,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer,
            explanation=explanation or "No explanation provided.",
            reference=f"Source: {quiz_title}"
        )

        questions.append(question)

    return questions


def import_html_quizzes(source_dir: str, db_path: str):
    """Import all HTML quiz files from a directory."""
    db = DatabaseManager(db_path)

    # Get all HTML files
    html_files = []
    for filename in os.listdir(source_dir):
        if filename.endswith('.html'):
            html_files.append(os.path.join(source_dir, filename))

    print(f"Found {len(html_files)} HTML files to process")

    total_imported = 0

    for filepath in html_files:
        filename = os.path.basename(filepath)
        print(f"\nProcessing: {filename}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()

            quiz_data = extract_quiz_data(html_content)

            if not quiz_data:
                print(f"  Could not extract quiz data from {filename}")
                continue

            quiz_title = quiz_data.get('quiz_title', 'Unknown')
            print(f"  Quiz: {quiz_title}")

            questions = parse_questions(quiz_data, filename)
            print(f"  Found {len(questions)} questions")

            # Import questions
            for q in questions:
                db.add_question(q)

            total_imported += len(questions)
            print(f"  Imported {len(questions)} questions")

        except Exception as e:
            print(f"  Error processing {filename}: {e}")

    print(f"\n{'='*50}")
    print(f"Total questions imported: {total_imported}")
    print(f"Total questions in database: {db.get_question_count('SAA-C03')}")


if __name__ == "__main__":
    import sys

    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, "quizz_add_sources")
    db_path = os.path.join(script_dir, "data", "questions.db")

    if not os.path.exists(source_dir):
        print(f"Source directory not found: {source_dir}")
        sys.exit(1)

    print(f"Source directory: {source_dir}")
    print(f"Database path: {db_path}")
    print()

    import_html_quizzes(source_dir, db_path)

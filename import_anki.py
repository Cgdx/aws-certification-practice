"""
Script to import Anki notes and generate exam questions from them.
"""
import os
import re
import html
import random
from database.db_manager import DatabaseManager
from database.models import Question

# Domain mapping based on content keywords
DOMAIN_KEYWORDS = {
    "1": ["iam", "security", "encryption", "kms", "cognito", "guard duty", "policy", "role", "mfa", "access key"],
    "2": ["rds", "aurora", "elasticache", "route 53", "multi-az", "replica", "failover", "backup", "disaster", "recovery", "high availability", "scalability", "load balancer"],
    "3": ["ec2", "s3", "ebs", "efs", "lambda", "dynamodb", "cloudfront", "vpc", "subnet", "kinesis", "sqs", "sns", "container", "ecs", "eks"],
    "4": ["cost", "pricing", "reserved", "spot", "savings", "budget", "architecture"]
}


def detect_domain(text: str) -> str:
    """Detect domain based on content keywords."""
    text_lower = text.lower()

    scores = {d: 0 for d in DOMAIN_KEYWORDS.keys()}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[domain] += 1

    max_score = max(scores.values())
    if max_score > 0:
        for domain, score in scores.items():
            if score == max_score:
                return domain

    return "3"  # Default to Domain 3


def clean_html_text(text: str) -> str:
    """Remove HTML tags and clean text."""
    if not text:
        return ""

    # Decode HTML entities
    text = html.unescape(text)

    # Replace <br> with newlines
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.strip()

    return text


def parse_cloze(text: str):
    """Parse cloze deletion text and extract blanks."""
    # Pattern to match {{c1::answer}} or {{c1::answer::hint}}
    pattern = r'\{\{c(\d+)::([^}]+?)(?:::([^}]+))?\}\}'

    matches = list(re.finditer(pattern, text))
    if not matches:
        return None, []

    # Get unique cloze numbers
    cloze_nums = sorted(set(int(m.group(1)) for m in matches))

    # Extract answers for each cloze number
    answers_by_num = {}
    for m in matches:
        num = int(m.group(1))
        answer = m.group(2)
        if num not in answers_by_num:
            answers_by_num[num] = []
        answers_by_num[num].append(answer)

    return cloze_nums, answers_by_num


def generate_cloze_question(text: str, cloze_num: int = 1):
    """Generate a question from cloze text for a specific cloze number."""
    pattern = r'\{\{c(\d+)::([^}]+?)(?:::([^}]+))?\}\}'

    correct_answers = []

    def replace_cloze(match):
        num = int(match.group(1))
        answer = match.group(2)
        hint = match.group(3)

        if num == cloze_num:
            correct_answers.append(answer)
            if hint:
                return f"[{hint}]"
            return "_____"
        else:
            return answer

    question_text = re.sub(pattern, replace_cloze, text)
    return question_text, correct_answers


def generate_mcq_from_cloze(text: str, all_answers: list):
    """Generate MCQ options from cloze text."""
    cloze_nums, answers_by_num = parse_cloze(text)
    if not cloze_nums:
        return None

    # Use first cloze
    cloze_num = cloze_nums[0]
    question_text, correct = generate_cloze_question(text, cloze_num)

    if not correct:
        return None

    correct_answer = correct[0] if len(correct) == 1 else " / ".join(correct)

    # Generate wrong answers from pool
    wrong_answers = [a for a in all_answers if a.lower() != correct_answer.lower()]
    random.shuffle(wrong_answers)
    wrong_answers = wrong_answers[:3]

    # If not enough wrong answers, generate generic ones
    while len(wrong_answers) < 3:
        wrong_answers.append(f"None of the above")
        break

    # Shuffle options
    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    correct_letter = chr(65 + options.index(correct_answer))

    formatted_options = [f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)]

    return {
        "question": clean_html_text(question_text),
        "options": formatted_options,
        "correct": correct_letter,
        "explanation": f"The correct answer is: {correct_answer}"
    }


def parse_anki_file(filepath: str):
    """Parse Anki export file and return cards."""
    cards = []
    all_cloze_answers = []  # Collect all answers for generating MCQ options

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip metadata lines
    data_lines = [l for l in lines if not l.startswith('#')]

    for line in data_lines:
        fields = line.strip().split('\t')
        if len(fields) < 5:
            continue

        guid = fields[0]
        note_type = fields[1]
        deck = fields[2]
        front = fields[3]
        back = fields[4] if len(fields) > 4 else ""

        # Skip image occlusion cards
        if note_type == "Image Occlusion Enhanced":
            continue

        # Collect cloze answers
        if note_type == "Cloze+":
            _, answers = parse_cloze(front)
            for ans_list in answers.values():
                all_cloze_answers.extend(ans_list)

        cards.append({
            "guid": guid,
            "type": note_type,
            "front": front,
            "back": back
        })

    return cards, list(set(all_cloze_answers))


def generate_questions_from_cards(cards: list, all_answers: list):
    """Generate exam questions from Anki cards."""
    questions = []

    for card in cards:
        note_type = card["type"]
        front = card["front"]
        back = card["back"]

        if note_type == "Basic++":
            # Convert to MCQ
            question_text = clean_html_text(front)
            correct_answer = clean_html_text(back)

            if not question_text or not correct_answer:
                continue

            # Skip if answer is too long (probably not suitable for MCQ)
            if len(correct_answer) > 200:
                continue

            # Generate wrong answers
            wrong = random.sample(all_answers, min(3, len(all_answers)))
            wrong = [w for w in wrong if w.lower() != correct_answer.lower()][:3]

            while len(wrong) < 3:
                wrong.append("None of the above")
                break

            options = [correct_answer] + wrong
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct_answer))

            questions.append({
                "question": question_text,
                "options": [f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)],
                "correct": correct_letter,
                "explanation": f"The correct answer is: {correct_answer}",
                "domain": detect_domain(question_text + " " + correct_answer)
            })

        elif note_type == "AWS services":
            # Service name -> description
            service_name = clean_html_text(front)
            description = clean_html_text(back)

            if not service_name or not description:
                continue

            question_text = f"What is AWS {service_name}?"

            # Get other service descriptions as wrong answers
            other_services = [c for c in cards if c["type"] == "AWS services" and c["front"] != front]
            wrong = [clean_html_text(s["back"]) for s in random.sample(other_services, min(3, len(other_services)))]

            while len(wrong) < 3:
                wrong.append("A deprecated AWS service")
                break

            options = [description] + wrong[:3]
            random.shuffle(options)
            correct_letter = chr(65 + options.index(description))

            questions.append({
                "question": question_text,
                "options": [f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)],
                "correct": correct_letter,
                "explanation": f"AWS {service_name}: {description}",
                "domain": detect_domain(service_name + " " + description)
            })

        elif note_type == "Cloze+":
            # Generate fill-in-blank MCQ
            mcq = generate_mcq_from_cloze(front, all_answers)
            if mcq:
                questions.append({
                    "question": mcq["question"],
                    "options": mcq["options"],
                    "correct": mcq["correct"],
                    "explanation": mcq["explanation"],
                    "domain": detect_domain(front)
                })

        elif note_type == "Code howto":
            # Convert CLI commands to questions
            action = clean_html_text(front)
            command = clean_html_text(back)

            if not action or not command:
                continue

            question_text = f"Which AWS CLI command would you use to {action}?"

            questions.append({
                "question": question_text,
                "options": [
                    f"A. {command}",
                    "B. aws help " + action.split()[0] if action.split() else "aws help",
                    "C. aws configure",
                    "D. aws sts get-caller-identity"
                ],
                "correct": "A",
                "explanation": f"The correct command is: {command}",
                "domain": "1"  # CLI is typically Domain 1
            })

    return questions


def import_anki_notes(filepath: str, db_path: str):
    """Import Anki notes into the database as exam questions."""
    print(f"Parsing Anki file: {filepath}")

    cards, all_answers = parse_anki_file(filepath)
    print(f"Found {len(cards)} cards")

    # Filter out very short answers
    all_answers = [a for a in all_answers if len(a) > 2 and len(a) < 100]
    print(f"Collected {len(all_answers)} unique answers for MCQ generation")

    questions = generate_questions_from_cards(cards, all_answers)
    print(f"Generated {len(questions)} questions")

    # Import to database
    db = DatabaseManager(db_path)
    imported = 0

    for q in questions:
        question = Question(
            id=0,
            exam_type="SAA-C03",
            domain=q["domain"],
            difficulty=2,  # Medium by default
            question_text=q["question"],
            options=q["options"],
            correct_answer=q["correct"],
            explanation=q["explanation"],
            reference="Source: Anki Notes"
        )
        db.add_question(question)
        imported += 1

    print(f"\nImported {imported} questions from Anki notes")
    print(f"Total questions in database: {db.get_question_count('SAA-C03')}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    anki_file = os.path.join(script_dir, "quizz_add_sources", "AWS Solutions Architect Associate.txt")
    db_path = os.path.join(script_dir, "data", "questions.db")

    if os.path.exists(anki_file):
        import_anki_notes(anki_file, db_path)
    else:
        print(f"Anki file not found: {anki_file}")

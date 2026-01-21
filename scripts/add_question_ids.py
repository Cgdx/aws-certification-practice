#!/usr/bin/env python3
"""
Script to add unique question IDs and fix multiple correct answers.
"""

import json
import re
import os

def detect_num_answers(question_text):
    """Detect how many answers are required from the question text."""
    text_lower = question_text.lower()

    # Patterns for multiple answers
    patterns = [
        (r'select\s+two', 2),
        (r'select\s+2', 2),
        (r'choose\s+two', 2),
        (r'choose\s+2', 2),
        (r'\(select\s+two\)', 2),
        (r'\(choose\s+two\)', 2),
        (r'select\s+three', 3),
        (r'select\s+3', 3),
        (r'choose\s+three', 3),
        (r'choose\s+3', 3),
    ]

    for pattern, num in patterns:
        if re.search(pattern, text_lower):
            return num

    return 1


def extract_correct_answers_from_explanation(explanation, num_expected, options=None):
    """Extract correct answer letters from explanation text."""
    if not explanation:
        return None

    answers = set()

    # Method 1: Look for explicit patterns like "A and E", "A, E"
    explicit_patterns = [
        r'\b([A-E])\s+(?:and|&)\s+([A-E])\b',
        r'\b([A-E])\s*,\s*([A-E])\b',
        r'Option\s+([A-E])\s+(?:and|&)\s+Option\s+([A-E])',
        r'Options?\s+([A-E])\s+(?:and|&)\s+([A-E])',
    ]

    for pattern in explicit_patterns:
        matches = re.findall(pattern, explanation, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                for m in match:
                    if m:
                        answers.add(m.upper())

    # Method 2: Look for "Why X is correct" patterns
    why_correct = re.findall(r'Why\s+([A-E])\s+(?:is|are)\s+correct', explanation, re.IGNORECASE)
    for letter in why_correct:
        answers.add(letter.upper())

    # Method 3: Look for "X is correct" at start of explanation or after section break
    is_correct = re.findall(r'(?:^|\n)\s*\*?\*?([A-E])\s+(?:is|are)\s+correct', explanation, re.IGNORECASE | re.MULTILINE)
    for letter in is_correct:
        answers.add(letter.upper())

    # Method 4: Look for "Correct Answer: X" or "Correct: X"
    correct_answer_pattern = re.findall(r'Correct\s*(?:Answer|Option)?s?[:\s]+([A-E])(?:\s*(?:and|,|&)\s*([A-E]))?', explanation, re.IGNORECASE)
    for match in correct_answer_pattern:
        if isinstance(match, tuple):
            for m in match:
                if m:
                    answers.add(m.upper())
        else:
            answers.add(match.upper())

    # Method 5: Match option text with explanation (for formats like "Use Amazon Aurora Replica")
    if options and len(answers) < num_expected:
        # Find section between "Correct options:" and "Incorrect options:"
        correct_section_match = re.search(
            r'Correct\s+options?[:\s](.*?)(?:Incorrect\s+options?|$)',
            explanation,
            re.IGNORECASE | re.DOTALL
        )

        if correct_section_match:
            correct_section = correct_section_match.group(1)

            for opt in options:
                # Extract the letter and text from option
                opt_match = re.match(r'^([A-E])[\.\)]\s*(.+)$', opt.strip())
                if opt_match:
                    letter = opt_match.group(1).upper()
                    opt_text = opt_match.group(2).strip()

                    # Get key words from option (first few significant words)
                    key_words = opt_text.split()[:4]
                    key_phrase = ' '.join(key_words)

                    # Check if this option is mentioned in correct section
                    if key_phrase.lower() in correct_section.lower():
                        answers.add(letter)

    # If we found the expected number of answers, return them
    if len(answers) == num_expected:
        return ','.join(sorted(answers))

    # If we found more than expected, try to be more selective
    if len(answers) > num_expected:
        return ','.join(sorted(answers)[:num_expected])

    # If we didn't find enough, return None to keep original
    return None


def process_questions(input_path, output_path):
    """Process questions to add IDs and fix multiple answers."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data['questions']
    print(f"Processing {len(questions)} questions...")

    # Track question IDs per exam type
    exam_counters = {}
    multi_answer_fixed = 0
    multi_answer_failed = []

    for i, q in enumerate(questions):
        exam_type = q.get('exam_type', 'SAA-C03')

        # Generate unique question_id
        if exam_type not in exam_counters:
            exam_counters[exam_type] = 0
        exam_counters[exam_type] += 1
        q['question_id'] = f"{exam_type}-{exam_counters[exam_type]:04d}"

        # Detect if multiple answers required
        question_text = q.get('question_text', '')
        num_correct = detect_num_answers(question_text)
        q['num_correct'] = num_correct

        if num_correct > 1:
            # Try to extract correct answers from explanation
            explanation = q.get('explanation', '')
            options = q.get('options', [])
            extracted = extract_correct_answers_from_explanation(explanation, num_correct, options)

            if extracted:
                q['correct_answer'] = extracted
                multi_answer_fixed += 1
                print(f"  Fixed {q['question_id']}: {extracted}")
            else:
                # Keep original but mark as needing review
                multi_answer_failed.append({
                    'question_id': q['question_id'],
                    'current_answer': q.get('correct_answer', ''),
                    'num_expected': num_correct,
                    'text_preview': question_text[:80]
                })

    print(f"\nProcessed {len(questions)} questions")
    print(f"Multi-answer questions fixed: {multi_answer_fixed}")
    print(f"Multi-answer questions needing manual review: {len(multi_answer_failed)}")

    # Save processed questions
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({'questions': questions}, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to: {output_path}")

    # Save list of questions needing manual review
    if multi_answer_failed:
        review_path = output_path.replace('.json', '_needs_review.json')
        with open(review_path, 'w', encoding='utf-8') as f:
            json.dump(multi_answer_failed, f, indent=2, ensure_ascii=False)
        print(f"Questions needing review saved to: {review_path}")

    return multi_answer_failed


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')

    input_path = os.path.join(data_dir, 'seed_questions.json')
    output_path = os.path.join(data_dir, 'seed_questions_with_ids.json')

    failed = process_questions(input_path, output_path)

    if failed:
        print("\n=== Questions needing manual review ===")
        for q in failed[:10]:
            print(f"\n{q['question_id']} (expects {q['num_expected']} answers, has: {q['current_answer']})")
            print(f"  {q['text_preview']}...")


if __name__ == '__main__':
    main()

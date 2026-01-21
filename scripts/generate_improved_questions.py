#!/usr/bin/env python3
"""
Final script to generate improved questions file.
Combines base questions + additional questions and improves explanations.
"""

import json
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from improve_questions import IMPROVED_ANKI_QUESTIONS
from additional_questions import ADDITIONAL_QUESTIONS

def format_explanation(question):
    """Format explanation with clear structure."""
    exp = question.get('explanation', '')
    correct = question.get('correct_answer', '')
    options = question.get('options', [])

    # If already well-formatted, return as-is
    if '**Why' in exp and '**Correct Answer' in exp:
        return exp

    # If explanation is empty or just "The correct answer is:"
    if not exp or 'The correct answer is:' in exp or len(exp) < 50:
        return generate_basic_explanation(question)

    # If explanation exists but needs formatting
    if len(exp) > 50 and '**' not in exp:
        formatted = f"**Correct Answer: {correct}**\n\n"
        formatted += f"**Why {correct} is correct:**\n{exp}\n"

        # Add placeholders for incorrect options
        for opt in options:
            letter = opt[0] if opt else ''
            if letter and letter != correct and letter in 'ABCDE':
                formatted += f"\n**Why {letter} is incorrect:**\nThis option does not meet the requirements specified in the question."

        return formatted

    return exp


def generate_basic_explanation(question):
    """Generate a basic explanation structure."""
    correct = question.get('correct_answer', '')
    options = question.get('options', [])
    q_text = question.get('question_text', '').lower()

    explanation = f"**Correct Answer: {correct}**\n\n"
    explanation += f"**Why {correct} is correct:**\n"
    explanation += "This option correctly addresses the requirements stated in the question.\n"

    for opt in options:
        letter = opt[0] if opt else ''
        if letter and letter != correct and letter in 'ABCDE':
            explanation += f"\n**Why {letter} is incorrect:**\n"
            explanation += "This option does not meet the specific requirements of the scenario."

    return explanation


def main():
    # Load current questions
    input_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed_questions.json')

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_questions = data['questions']
    print(f"Loaded {len(original_questions)} original questions")

    # Separate questions by source
    practice_test_questions = []  # Keep as-is (good quality)
    aws_docs_questions = []  # Keep as-is (good quality)
    quiz_questions = []  # Need explanation improvements
    anki_questions = []  # Replace entirely

    for q in original_questions:
        ref = q.get('reference', '')
        if 'Practice Test' in ref:
            practice_test_questions.append(q)
        elif ref.startswith('https://'):
            aws_docs_questions.append(q)
        elif 'Anki' in ref:
            anki_questions.append(q)
        else:
            quiz_questions.append(q)

    print(f"Practice Test questions (keeping as-is): {len(practice_test_questions)}")
    print(f"AWS Docs questions (keeping as-is): {len(aws_docs_questions)}")
    print(f"Quiz questions (improving explanations): {len(quiz_questions)}")
    print(f"Anki questions (replacing): {len(anki_questions)}")

    # Improve explanations for quiz questions
    for q in quiz_questions:
        q['explanation'] = format_explanation(q)

    # Combine all improved questions
    all_improved_questions = IMPROVED_ANKI_QUESTIONS + ADDITIONAL_QUESTIONS
    print(f"New replacement questions: {len(all_improved_questions)}")

    # Final question set
    final_questions = (
        practice_test_questions +
        aws_docs_questions +
        quiz_questions +
        all_improved_questions
    )

    print(f"\nFinal question count: {len(final_questions)}")

    # Save to new file
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed_questions_improved.json')

    output_data = {'questions': final_questions}

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved improved questions to: {output_path}")
    print("\nTo apply changes:")
    print("1. Backup: copy seed_questions.json to seed_questions_backup.json")
    print("2. Replace: copy seed_questions_improved.json to seed_questions.json")
    print("3. Delete the database: delete data/questions.db")
    print("4. Restart the app to reload questions")


if __name__ == '__main__':
    main()

import streamlit as st
from database.models import Question, DOMAINS
from typing import Union, List


def render_question(question: Question, question_number: int, total_questions: int,
                    current_answer: Union[str, List[str]] = None, show_result: bool = False,
                    marked_for_review: bool = False):
    """Render a single question with options. Supports single and multiple answer questions."""

    domain_name = DOMAINS.get(question.domain, f"Domain {question.domain}")
    difficulty_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
    difficulty_colors = {1: "green", 2: "orange", 3: "red"}

    # Get correct answers as list
    correct_answers = question.correct_answers_list
    is_multi_answer = question.is_multiple_choice

    # Normalize current_answer to list
    if current_answer is None:
        current_answers = []
    elif isinstance(current_answer, str):
        current_answers = [a.strip() for a in current_answer.split(',') if a.strip()]
    else:
        current_answers = list(current_answer)

    # Header with question info
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"**Question {question_number} of {total_questions}**")
    with col2:
        st.markdown(f"Domain: **{domain_name}**")
    with col3:
        diff_label = difficulty_labels.get(question.difficulty, "Unknown")
        diff_color = difficulty_colors.get(question.difficulty, "gray")
        st.markdown(f"Difficulty: :{diff_color}[**{diff_label}**]")
    with col4:
        if question.question_id:
            st.markdown(f"ID: `{question.question_id}`")

    st.markdown("---")

    # Question text
    st.markdown(f"### {question.question_text}")

    # Show instruction for multi-answer questions
    if is_multi_answer:
        st.info(f"Select **{question.num_correct}** answers")

    st.markdown("")

    selected_answers = []

    if show_result and current_answers:
        # Show results mode
        for i, option in enumerate(question.options):
            option_letter = option[0] if option else chr(65 + i)

            is_correct = option_letter in correct_answers
            is_selected = option_letter in current_answers

            if is_correct and is_selected:
                st.success(f"✓ {option}")
            elif is_correct and not is_selected:
                st.warning(f"✓ {option} (correct, not selected)")
            elif is_selected and not is_correct:
                st.error(f"✗ {option}")
            else:
                st.markdown(f"  {option}")

        st.markdown("---")

        # Check if answer is fully correct
        user_correct = set(current_answers) == set(correct_answers)

        if user_correct:
            st.success("Correct!")
        else:
            correct_display = ', '.join(correct_answers)
            st.error(f"Incorrect. The correct answer(s): **{correct_display}**")

        with st.expander("View Explanation", expanded=True):
            st.markdown(question.explanation)
            if question.reference:
                st.markdown(f"[AWS Documentation]({question.reference})")

        selected_answers = current_answers
    else:
        # Answer selection mode
        if is_multi_answer:
            # Use checkboxes for multiple answers
            st.markdown("**Select your answers:**")
            for i, option in enumerate(question.options):
                option_letter = option[0] if option else chr(65 + i)
                is_checked = option_letter in current_answers

                if st.checkbox(
                    option,
                    value=is_checked,
                    key=f"q_{question.id}_opt_{option_letter}"
                ):
                    if option_letter not in selected_answers:
                        selected_answers.append(option_letter)
                elif option_letter in selected_answers:
                    selected_answers.remove(option_letter)

            # Also check session state for checkbox values
            for i, option in enumerate(question.options):
                option_letter = option[0] if option else chr(65 + i)
                key = f"q_{question.id}_opt_{option_letter}"
                if key in st.session_state and st.session_state[key]:
                    if option_letter not in selected_answers:
                        selected_answers.append(option_letter)

            # Show selection count
            if selected_answers:
                count = len(selected_answers)
                if count < question.num_correct:
                    st.caption(f"Selected {count}/{question.num_correct} answers")
                elif count == question.num_correct:
                    st.caption(f"Selected {count}/{question.num_correct} answers ✓")
                else:
                    st.warning(f"Selected {count}/{question.num_correct} answers (too many)")
        else:
            # Use radio buttons for single answer
            options_list = question.options

            default_index = None
            if current_answers:
                for i, option in enumerate(question.options):
                    if option[0] in current_answers:
                        default_index = i
                        break

            selected = st.radio(
                "Select your answer:",
                options=options_list,
                index=default_index,
                key=f"q_{question.id}"
            )

            if selected:
                selected_answers = [selected[0]]

    # Return as comma-separated string for consistency
    result_answer = ','.join(sorted(selected_answers)) if selected_answers else None
    return result_answer, marked_for_review


def render_navigation(question_number: int, total_questions: int,
                      marked_questions: set, answered_questions: set):
    """Render question navigation controls."""

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        prev_disabled = question_number <= 1
        prev_clicked = st.button("Previous", disabled=prev_disabled, use_container_width=True)

    with col2:
        next_disabled = question_number >= total_questions
        next_clicked = st.button("Next", disabled=next_disabled, use_container_width=True)

    with col3:
        is_marked = question_number in marked_questions
        mark_label = "Unmark" if is_marked else "Mark for Review"
        mark_clicked = st.button(mark_label, use_container_width=True)

    with col4:
        submit_clicked = st.button("Submit Exam", type="primary", use_container_width=True)

    st.markdown("---")

    st.markdown("### Question Navigator")

    cols = st.columns(10)
    for i in range(total_questions):
        q_num = i + 1
        col_idx = i % 10

        with cols[col_idx]:
            if q_num in answered_questions:
                if q_num in marked_questions:
                    btn_type = "Mark"
                    style = "background-color: orange;"
                else:
                    btn_type = "Done"
                    style = "background-color: green;"
            else:
                if q_num in marked_questions:
                    btn_type = "Mark"
                    style = "background-color: orange;"
                else:
                    btn_type = ""
                    style = ""

            if st.button(str(q_num), key=f"nav_{q_num}", use_container_width=True):
                return {"action": "goto", "question": q_num}

    st.markdown(f"""
    **Legend:** Answered: {len(answered_questions)}/{total_questions} |
    Marked for review: {len(marked_questions)}
    """)

    if prev_clicked:
        return {"action": "prev"}
    if next_clicked:
        return {"action": "next"}
    if mark_clicked:
        return {"action": "mark"}
    if submit_clicked:
        return {"action": "submit"}

    return None

import streamlit as st
from database.models import Question, DOMAINS


def render_question(question: Question, question_number: int, total_questions: int,
                    current_answer: str = None, show_result: bool = False,
                    marked_for_review: bool = False):
    """Render a single question with options."""

    domain_name = DOMAINS.get(question.domain, f"Domain {question.domain}")
    difficulty_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
    difficulty_colors = {1: "green", 2: "orange", 3: "red"}

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Question {question_number} of {total_questions}**")
    with col2:
        st.markdown(f"Domain: **{domain_name}**")
    with col3:
        diff_label = difficulty_labels.get(question.difficulty, "Unknown")
        diff_color = difficulty_colors.get(question.difficulty, "gray")
        st.markdown(f"Difficulty: :{diff_color}[**{diff_label}**]")

    st.markdown("---")

    st.markdown(f"### {question.question_text}")

    st.markdown("")

    selected_answer = None

    if show_result and current_answer:
        for i, option in enumerate(question.options):
            option_letter = option[0] if option else chr(65 + i)

            is_correct = option_letter == question.correct_answer
            is_selected = option_letter == current_answer

            if is_correct:
                st.success(f"{option}")
            elif is_selected and not is_correct:
                st.error(f"{option}")
            else:
                st.markdown(f"{option}")

        st.markdown("---")

        if current_answer == question.correct_answer:
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answer is: **{question.correct_answer}**")

        with st.expander("View Explanation", expanded=True):
            st.markdown(question.explanation)
            if question.reference:
                st.markdown(f"[AWS Documentation]({question.reference})")
    else:
        options_list = []
        for i, option in enumerate(question.options):
            options_list.append(option)

        default_index = None
        if current_answer:
            for i, option in enumerate(question.options):
                if option.startswith(current_answer):
                    default_index = i
                    break

        selected = st.radio(
            "Select your answer:",
            options=options_list,
            index=default_index,
            key=f"q_{question.id}"
        )

        if selected:
            selected_answer = selected[0]

    return selected_answer, marked_for_review


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

import streamlit as st
from database.models import EXAM_CONFIG, EXAM_DOMAINS


def render_exam_selector(question_counts: dict):
    """Render the exam selection screen."""
    st.title("Practice Exam")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Select Exam Type")
        exam_type = st.selectbox(
            "Choose your certification exam:",
            options=list(EXAM_CONFIG.keys()),
            format_func=lambda x: f"{x} - {EXAM_CONFIG[x]['name']}"
        )

        config = EXAM_CONFIG[exam_type]
        is_available = config.get('available', True)
        question_count = question_counts.get(exam_type, 0)

        # Show warning if exam not available
        if not is_available:
            st.warning("This exam is coming soon. Questions are not yet available in the database.")

        st.markdown("### Exam Information")
        st.markdown(f"""
        - **Exam:** {config['name']}
        - **Total Questions:** {config['total_questions']} ({config['scored_questions']} scored)
        - **Time Limit:** {config['time_minutes']} minutes
        - **Passing Score:** {config['passing_score']}/1000 (~{config['passing_percentage']}%)
        - **Questions in Database:** {question_count}
        """)

        st.markdown("### Exam Domains")
        domains = EXAM_DOMAINS.get(exam_type, {})
        for domain_id, domain_info in domains.items():
            st.markdown(f"- **Domain {domain_id}:** {domain_info['name']} ({domain_info['weight']}%)")

    with col2:
        st.subheader("Practice Mode")

        # Disable mode selection if exam not available
        mode = st.radio(
            "Select practice mode:",
            options=["full", "practice_10", "practice_20", "practice_30"],
            format_func=lambda x: {
                "full": f"Full Exam ({min(config['total_questions'], question_count)} questions)",
                "practice_10": "Quick Practice (10 questions)",
                "practice_20": "Short Practice (20 questions)",
                "practice_30": "Medium Practice (30 questions)"
            }[x],
            disabled=not is_available
        )

        num_questions = {
            "full": min(config['total_questions'], question_count),
            "practice_10": min(10, question_count),
            "practice_20": min(20, question_count),
            "practice_30": min(30, question_count)
        }[mode]

        timed = st.checkbox("Enable Timer", value=True, disabled=not is_available)

        if timed and is_available:
            if mode == "full":
                time_minutes = config['time_minutes']
            else:
                time_minutes = int(num_questions * 2)
            st.info(f"Time allowed: {time_minutes} minutes")
        else:
            time_minutes = 0

        st.markdown("---")

        # Spaced Repetition Mode
        st.subheader("Spaced Repetition")
        spaced_repetition = st.checkbox(
            "Use Spaced Repetition",
            value=False,
            help="Prioritize questions you need to review based on your past performance (like Anki)",
            disabled=not is_available
        )

        if spaced_repetition and is_available:
            st.info("Questions due for review will be prioritized. Rate your confidence after each answer to improve future sessions.")

        st.markdown("---")

        # Disable Start button if exam not available or no questions
        can_start = is_available and question_count > 0
        if st.button("Start Exam", type="primary", use_container_width=True, disabled=not can_start):
            return {
                "exam_type": exam_type,
                "mode": mode,
                "num_questions": num_questions,
                "timed": timed,
                "time_minutes": time_minutes,
                "spaced_repetition": spaced_repetition
            }

    return None

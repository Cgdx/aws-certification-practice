import streamlit as st
from database.models import EXAM_CONFIG, DOMAINS, DOMAIN_WEIGHTS


def render_exam_selector(question_count: int):
    """Render the exam selection screen."""
    st.title("AWS Certification Practice Exam")
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

        st.markdown("### Exam Information")
        st.markdown(f"""
        - **Exam:** {config['name']}
        - **Total Questions:** {config['total_questions']} ({config['scored_questions']} scored)
        - **Time Limit:** {config['time_minutes']} minutes
        - **Passing Score:** {config['passing_score']}/1000 (~{config['passing_percentage']}%)
        - **Questions in Database:** {question_count}
        """)

        st.markdown("### Exam Domains")
        for domain_id, domain_name in DOMAINS.items():
            weight = DOMAIN_WEIGHTS[domain_id]
            st.markdown(f"- **Domain {domain_id}:** {domain_name} ({weight}%)")

    with col2:
        st.subheader("Practice Mode")

        mode = st.radio(
            "Select practice mode:",
            options=["full", "practice_10", "practice_20", "practice_30"],
            format_func=lambda x: {
                "full": f"Full Exam ({min(config['total_questions'], question_count)} questions)",
                "practice_10": "Quick Practice (10 questions)",
                "practice_20": "Short Practice (20 questions)",
                "practice_30": "Medium Practice (30 questions)"
            }[x]
        )

        num_questions = {
            "full": min(config['total_questions'], question_count),
            "practice_10": min(10, question_count),
            "practice_20": min(20, question_count),
            "practice_30": min(30, question_count)
        }[mode]

        timed = st.checkbox("Enable Timer", value=True)

        if timed:
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
            help="Prioritize questions you need to review based on your past performance (like Anki)"
        )

        if spaced_repetition:
            st.info("Questions due for review will be prioritized. Rate your confidence after each answer to improve future sessions.")

        st.markdown("---")

        if st.button("Start Exam", type="primary", use_container_width=True):
            return {
                "exam_type": exam_type,
                "mode": mode,
                "num_questions": num_questions,
                "timed": timed,
                "time_minutes": time_minutes,
                "spaced_repetition": spaced_repetition
            }

    return None

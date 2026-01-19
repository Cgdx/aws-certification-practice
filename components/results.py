import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from database.models import Question, ExamSession, DOMAINS, DOMAIN_WEIGHTS, EXAM_CONFIG
from utils.scoring import calculate_domain_scores, identify_weak_domains
from components.timer import format_time


def render_results(questions: list, answers: dict, exam_type: str,
                   time_spent: int, session: ExamSession = None):
    """Render the exam results page."""

    st.title("Exam Results")
    st.markdown("---")

    correct_count = sum(
        1 for q in questions
        if answers.get(q.id) == q.correct_answer
    )
    total = len(questions)
    percentage = (correct_count / total) * 100 if total > 0 else 0

    config = EXAM_CONFIG.get(exam_type, {})
    passing_percentage = config.get('passing_percentage', 72)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Score", f"{correct_count}/{total}")

    with col2:
        delta_color = "normal" if percentage >= passing_percentage else "inverse"
        st.metric(
            "Percentage",
            f"{percentage:.1f}%",
            delta=f"{percentage - passing_percentage:.1f}% from passing",
            delta_color=delta_color
        )

    with col3:
        st.metric("Time Spent", format_time(time_spent))

    if percentage >= passing_percentage:
        st.success(f"Congratulations! You passed the exam with {percentage:.1f}%!")
    else:
        st.error(f"You need {passing_percentage}% to pass. Keep studying!")

    st.markdown("---")
    st.subheader("Performance by Domain")

    domain_scores = calculate_domain_scores(questions, answers)

    domain_data = []
    for domain_id, (correct, total_domain) in domain_scores.items():
        domain_name = DOMAINS.get(domain_id, f"Domain {domain_id}")
        pct = (correct / total_domain * 100) if total_domain > 0 else 0
        weight = DOMAIN_WEIGHTS.get(domain_id, 0)
        domain_data.append({
            "Domain": f"D{domain_id}: {domain_name[:30]}...",
            "Full Name": domain_name,
            "Correct": correct,
            "Total": total_domain,
            "Percentage": pct,
            "Weight": weight
        })

    df = pd.DataFrame(domain_data)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Domain"],
        y=df["Percentage"],
        name="Your Score",
        marker_color=["green" if p >= passing_percentage else "red" for p in df["Percentage"]],
        text=[f"{p:.0f}%" for p in df["Percentage"]],
        textposition="outside"
    ))

    fig.add_hline(
        y=passing_percentage,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Passing: {passing_percentage}%"
    )

    fig.update_layout(
        title="Score by Domain",
        xaxis_title="Domain",
        yaxis_title="Percentage",
        yaxis_range=[0, 100],
        showlegend=False,
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Domain Details")
        for item in domain_data:
            with st.expander(f"{item['Full Name']} ({item['Weight']}% of exam)"):
                st.markdown(f"**Score:** {item['Correct']}/{item['Total']} ({item['Percentage']:.1f}%)")
                if item['Percentage'] < passing_percentage:
                    st.warning("This domain needs more study!")
                else:
                    st.success("Good performance in this domain!")

    with col2:
        weak_domains = identify_weak_domains(domain_scores, passing_percentage)
        st.subheader("Areas to Improve")
        if weak_domains:
            for domain_id in weak_domains:
                domain_name = DOMAINS.get(domain_id, f"Domain {domain_id}")
                st.markdown(f"- **Domain {domain_id}:** {domain_name}")
        else:
            st.success("Great job! All domains above passing threshold.")

    st.markdown("---")
    st.subheader("Question Review")

    filter_option = st.radio(
        "Filter questions:",
        options=["all", "incorrect", "correct"],
        format_func=lambda x: {"all": "All Questions", "incorrect": "Incorrect Only", "correct": "Correct Only"}[x],
        horizontal=True
    )

    for i, q in enumerate(questions):
        user_answer = answers.get(q.id, "Not answered")
        is_correct = user_answer == q.correct_answer

        if filter_option == "incorrect" and is_correct:
            continue
        if filter_option == "correct" and not is_correct:
            continue

        domain_name = DOMAINS.get(q.domain, f"Domain {q.domain}")

        with st.expander(
            f"Q{i + 1}: {'Correct' if is_correct else 'Incorrect'} - {q.question_text[:50]}...",
            expanded=not is_correct
        ):
            st.markdown(f"**Domain:** {domain_name}")
            st.markdown(f"**Difficulty:** {'Easy' if q.difficulty == 1 else 'Medium' if q.difficulty == 2 else 'Hard'}")
            st.markdown(f"**Question:** {q.question_text}")

            st.markdown("**Options:**")
            for option in q.options:
                option_letter = option[0]
                if option_letter == q.correct_answer:
                    st.markdown(f"- :green[{option}] (Correct)")
                elif option_letter == user_answer:
                    st.markdown(f"- :red[{option}] (Your answer)")
                else:
                    st.markdown(f"- {option}")

            st.markdown(f"**Explanation:** {q.explanation}")
            if q.reference:
                st.markdown(f"[AWS Documentation]({q.reference})")


def render_history(sessions: list):
    """Render exam history."""
    st.subheader("Exam History")

    if not sessions:
        st.info("No previous exam sessions found.")
        return

    for session in sessions:
        with st.expander(f"{session.date.strftime('%Y-%m-%d %H:%M')} - {session.percentage:.1f}%"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{session.score}/{session.total}")
            with col2:
                st.metric("Percentage", f"{session.percentage:.1f}%")
            with col3:
                st.metric("Time", format_time(session.time_spent))

            if session.weak_domains:
                st.markdown("**Weak domains:**")
                for domain_id in session.weak_domains:
                    domain_name = DOMAINS.get(domain_id, f"Domain {domain_id}")
                    st.markdown(f"- {domain_name}")

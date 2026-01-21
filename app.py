import streamlit as st
import os
from datetime import datetime

from database.db_manager import DatabaseManager
from database.models import Question, ExamSession, EXAM_CONFIG
from components.exam_selector import render_exam_selector
from components.question_display import render_question, render_navigation
from components.timer import render_timer, get_elapsed_time
from components.results import render_results, render_history
from components.auth_ui import render_auth_page, render_user_info
from components.profile import render_profile_page
from components.leaderboard import render_leaderboard_page
from components.public_profile import render_public_profile_page
from auth import AuthManager, User
from utils.scoring import calculate_score, calculate_domain_scores, identify_weak_domains, is_answer_correct

st.set_page_config(
    page_title="Practice Exam",
    page_icon="",
    layout="wide"
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DATA_DIR, "questions.db")
SEED_PATH = os.path.join(DATA_DIR, "seed_questions.json")


@st.cache_resource
def get_db_manager():
    """Get or create database manager instance."""
    db = DatabaseManager(DB_PATH)

    if db.get_question_count("SAA-C03") == 0 and os.path.exists(SEED_PATH):
        db.import_questions_from_json(SEED_PATH)

    return db


@st.cache_resource
def get_auth_manager():
    """Get or create authentication manager instance."""
    return AuthManager(DB_PATH)


def init_session_state():
    """Initialize session state variables."""
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "exam_config" not in st.session_state:
        st.session_state.exam_config = None
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "marked_questions" not in st.session_state:
        st.session_state.marked_questions = set()
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "checked_questions" not in st.session_state:
        st.session_state.checked_questions = set()
    if "rated_questions" not in st.session_state:
        st.session_state.rated_questions = set()
    if "show_submit_confirm" not in st.session_state:
        st.session_state.show_submit_confirm = False
    # Authentication state
    if "user" not in st.session_state:
        st.session_state.user = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None


def start_exam(db: DatabaseManager, config: dict):
    """Start a new exam session."""
    exam_type = config["exam_type"]
    num_questions = config["num_questions"]
    use_spaced_repetition = config.get("spaced_repetition", False)
    user_id = st.session_state.user_id or 1

    if use_spaced_repetition:
        # Use spaced repetition algorithm to select questions
        questions = db.get_questions_for_review(exam_type, limit=num_questions, user_id=user_id)
    else:
        questions = db.get_questions_by_exam(exam_type, limit=num_questions)
        questions.sort(key=lambda q: (q.difficulty, q.id))

    st.session_state.exam_config = config
    st.session_state.questions = questions
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.marked_questions = set()
    st.session_state.start_time = datetime.now()
    st.session_state.show_result = False
    st.session_state.submitted = False
    st.session_state.checked_questions = set()
    st.session_state.rated_questions = set()
    st.session_state.show_submit_confirm = False
    st.session_state.page = "exam"


def submit_exam(db: DatabaseManager):
    """Submit the exam and save results."""
    questions = st.session_state.questions
    answers = st.session_state.answers
    config = st.session_state.exam_config
    user_id = st.session_state.user_id or 1

    correct, total = calculate_score(questions, answers)
    domain_scores = calculate_domain_scores(questions, answers)
    weak_domains = identify_weak_domains(domain_scores)

    time_spent = get_elapsed_time(st.session_state.start_time)

    session = ExamSession(
        id=0,
        exam_type=config["exam_type"],
        date=datetime.now(),
        score=correct,
        total=total,
        time_spent=time_spent,
        weak_domains=weak_domains
    )

    db.save_exam_session(session, user_id=user_id)

    st.session_state.submitted = True
    st.session_state.page = "results"


def render_exam_page(db: DatabaseManager, auth_manager):
    """Render the exam taking page."""
    config = st.session_state.exam_config
    questions = st.session_state.questions
    current_idx = st.session_state.current_question

    if not questions:
        st.error("No questions available. Please return to home.")
        if st.button("Return to Home"):
            st.session_state.page = "home"
            st.rerun()
        return

    question = questions[current_idx]
    total = len(questions)

    col1, col2 = st.columns([3, 1])

    with col2:
        if config.get("timed") and config.get("time_minutes", 0) > 0:
            time_expired, elapsed = render_timer(
                st.session_state.start_time,
                config["time_minutes"]
            )
            if time_expired and not st.session_state.submitted:
                submit_exam(db)
                st.rerun()

        st.markdown("---")

        progress = len(st.session_state.answers) / total
        st.progress(progress)
        st.caption(f"Answered: {len(st.session_state.answers)}/{total}")

        if st.button("End Exam", type="secondary", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with col1:
        current_answer = st.session_state.answers.get(question.id)
        is_marked = (current_idx + 1) in st.session_state.marked_questions

        selected_answer, _ = render_question(
            question=question,
            question_number=current_idx + 1,
            total_questions=total,
            current_answer=current_answer,
            show_result=st.session_state.show_result,
            marked_for_review=is_marked
        )

        if selected_answer and not st.session_state.show_result:
            st.session_state.answers[question.id] = selected_answer

        st.markdown("---")

        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            if st.button("Previous", disabled=current_idx == 0, use_container_width=True):
                st.session_state.show_result = False
                st.session_state.current_question = max(0, current_idx - 1)
                st.rerun()

        with col_b:
            if st.button("Next", disabled=current_idx >= total - 1, use_container_width=True):
                st.session_state.show_result = False
                st.session_state.current_question = min(total - 1, current_idx + 1)
                st.rerun()

        with col_c:
            q_num = current_idx + 1
            is_marked = q_num in st.session_state.marked_questions
            mark_label = "Unmark" if is_marked else "Mark"
            if st.button(mark_label, use_container_width=True):
                if is_marked:
                    st.session_state.marked_questions.discard(q_num)
                else:
                    st.session_state.marked_questions.add(q_num)
                st.rerun()

        with col_d:
            if not st.session_state.show_result:
                if st.button("Check Answer", use_container_width=True,
                            disabled=question.id not in st.session_state.answers):
                    st.session_state.show_result = True
                    st.session_state.checked_questions.add(question.id)
                    st.rerun()
            else:
                if st.button("Hide Answer", use_container_width=True):
                    st.session_state.show_result = False
                    st.rerun()

        # Show rating buttons after checking answer (for spaced repetition)
        if st.session_state.show_result and question.id not in st.session_state.rated_questions:
            user_answer = st.session_state.answers.get(question.id, '')
            was_correct = is_answer_correct(user_answer, question.correct_answer)

            st.markdown("---")
            st.markdown("**Rate your confidence:** _(for spaced repetition)_")

            # Show XP info
            if was_correct:
                base_xp = 10 + (question.difficulty * 2)
                st.caption(f"Correct! You'll earn XP based on your rating.")
            else:
                st.caption("Incorrect - No XP awarded. Keep practicing!")

            rate_cols = st.columns(4)

            user_id = st.session_state.user_id or 1

            # XP awards: correct answers get XP, rating affects bonus
            # Again: +2 XP, Hard: +5 XP, Good: +10 XP, Easy: +15 XP
            xp_rewards = {1: 2, 2: 5, 3: 10, 4: 15}

            with rate_cols[0]:
                if st.button("Again", key=f"rate_1_{question.id}", use_container_width=True,
                            help="Review again soon (+2 XP if correct)"):
                    db.update_question_stats(question.id, was_correct, 1, user_id=user_id)
                    if was_correct:
                        auth_manager.add_experience(user_id, xp_rewards[1])
                    st.session_state.rated_questions.add(question.id)
                    st.rerun()

            with rate_cols[1]:
                if st.button("Hard", key=f"rate_2_{question.id}", use_container_width=True,
                            help="Was difficult, review sooner (+5 XP if correct)"):
                    db.update_question_stats(question.id, was_correct, 2, user_id=user_id)
                    if was_correct:
                        auth_manager.add_experience(user_id, xp_rewards[2])
                    st.session_state.rated_questions.add(question.id)
                    st.rerun()

            with rate_cols[2]:
                if st.button("Good", key=f"rate_3_{question.id}", use_container_width=True,
                            help="Normal review interval (+10 XP if correct)"):
                    db.update_question_stats(question.id, was_correct, 3, user_id=user_id)
                    if was_correct:
                        auth_manager.add_experience(user_id, xp_rewards[3])
                    st.session_state.rated_questions.add(question.id)
                    st.rerun()

            with rate_cols[3]:
                if st.button("Easy", key=f"rate_4_{question.id}", use_container_width=True,
                            help="Too easy, review later (+15 XP if correct)"):
                    db.update_question_stats(question.id, was_correct, 4, user_id=user_id)
                    if was_correct:
                        auth_manager.add_experience(user_id, xp_rewards[4])
                    st.session_state.rated_questions.add(question.id)
                    st.rerun()

        elif st.session_state.show_result and question.id in st.session_state.rated_questions:
            st.success("Rating saved for spaced repetition!")

        st.markdown("---")

        st.markdown("### Question Navigator")

        cols = st.columns(13)
        for i in range(total):
            q_num = i + 1
            col_idx = i % 13

            q = questions[i]
            is_answered = q.id in st.session_state.answers
            is_checked = q.id in st.session_state.checked_questions
            is_current = i == current_idx
            is_marked_q = q_num in st.session_state.marked_questions

            # Check if answer is correct (only matters if checked)
            user_answer = st.session_state.answers.get(q.id, '')
            is_correct = is_answer_correct(user_answer, q.correct_answer) if user_answer else False

            with cols[col_idx]:
                # Determine background color based on answer status
                if is_marked_q:
                    # Marked questions shown in orange
                    bg_color = "orange"
                    text_color = "black"
                elif is_checked:
                    # Only show correct/incorrect after "Check Answer" clicked
                    if is_correct:
                        # Correct answer: green
                        bg_color = "#28a745"
                        text_color = "white"
                    else:
                        # Wrong answer: red
                        bg_color = "#dc3545"
                        text_color = "white"
                elif is_answered:
                    # Answered but not yet checked: blue
                    bg_color = "#007bff"
                    text_color = "white"
                else:
                    # Not answered: gray
                    bg_color = "#6c757d"
                    text_color = "white"

                # Add border for current question
                border_style = "border: 3px solid #007bff;" if is_current else ""

                st.markdown(
                    f"<div style='text-align:center;background-color:{bg_color};color:{text_color};"
                    f"padding:5px;border-radius:5px;{border_style}'>"
                    f"<b>{q_num}</b></div>",
                    unsafe_allow_html=True
                )

                if st.button(" ", key=f"nav_{q_num}", use_container_width=True):
                    st.session_state.show_result = False
                    st.session_state.current_question = i
                    st.rerun()

        st.markdown("---")

        unanswered = total - len(st.session_state.answers)

        if not st.session_state.show_submit_confirm:
            if st.button("Submit Exam", type="primary", use_container_width=True):
                if unanswered > 0:
                    st.session_state.show_submit_confirm = True
                    st.rerun()
                else:
                    submit_exam(db)
                    st.rerun()
        else:
            st.warning(f"You have {unanswered} unanswered questions. Are you sure you want to submit?")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("Yes, Submit", type="primary", use_container_width=True):
                    st.session_state.show_submit_confirm = False
                    submit_exam(db)
                    st.rerun()
            with col_no:
                if st.button("No, Continue", use_container_width=True):
                    st.session_state.show_submit_confirm = False
                    st.rerun()


def render_results_page(db: DatabaseManager):
    """Render the results page."""
    questions = st.session_state.questions
    answers = st.session_state.answers
    config = st.session_state.exam_config
    time_spent = get_elapsed_time(st.session_state.start_time)

    render_results(
        questions=questions,
        answers=answers,
        exam_type=config["exam_type"],
        time_spent=time_spent
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start New Exam", type="primary", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with col2:
        if st.button("View History", use_container_width=True):
            user_id = st.session_state.user_id or 1
            sessions = db.get_exam_sessions(config["exam_type"], user_id=user_id)
            render_history(sessions)


def main():
    """Main application entry point."""
    init_session_state()

    db = get_db_manager()
    auth_manager = get_auth_manager()

    # Check if user is authenticated
    if st.session_state.user is None:
        user = render_auth_page(auth_manager)
        if user:
            st.session_state.user = user
            st.session_state.user_id = user.id
            st.rerun()
        return

    # User is authenticated - show main app
    user = st.session_state.user
    user_id = st.session_state.user_id

    with st.sidebar:
        # Header with title and sign out button
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.title("Practice Exam")
        with header_col2:
            st.write("")  # Spacer
            if st.button("🚪", help="Sign Out", use_container_width=True):
                if 'user' in st.session_state:
                    del st.session_state['user']
                if 'user_id' in st.session_state:
                    del st.session_state['user_id']
                st.rerun()

        st.markdown("---")

        # Navigation menu - vertical with icons and titles
        if st.button("🏠  Home", use_container_width=True, type="secondary"):
            st.session_state.page = "home"
            st.rerun()

        if st.button("👤  Profile", use_container_width=True, type="secondary"):
            st.session_state.page = "profile"
            st.rerun()

        if st.button("🏆  Ranking", use_container_width=True, type="secondary"):
            st.session_state.page = "leaderboard"
            st.rerun()

        st.markdown("---")

        # Learning progress for current user
        st.markdown("### Learning Progress")
        progress = db.get_learning_progress("SAA-C03", user_id=user_id)

        st.metric("Total Questions", progress["total"])

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.metric("Seen", progress["seen"])
            st.metric("Due", progress["due_for_review"])
        with col_p2:
            st.metric("New", progress["new"])
            st.metric("Mastered", progress["mastered"])

        if progress["seen"] > 0:
            st.progress(progress["avg_success_rate"] / 100)
            st.caption(f"Success rate: {progress['avg_success_rate']:.1f}%")

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        Practice for your AWS certification exam with realistic questions
        covering all domains.

        **Features:**
        - Timed exams
        - Difficulty progression
        - Domain-based scoring
        - Detailed explanations
        """)

        st.markdown("---")
        st.caption("© Practice Exams 2026")

    if st.session_state.page == "home":
        # Get question counts for all exam types
        question_counts = {
            exam_type: db.get_question_count(exam_type)
            for exam_type in EXAM_CONFIG.keys()
        }
        config = render_exam_selector(question_counts)
        if config:
            start_exam(db, config)
            st.rerun()

    elif st.session_state.page == "exam":
        render_exam_page(db, auth_manager)

    elif st.session_state.page == "results":
        render_results_page(db)

    elif st.session_state.page == "profile":
        render_profile_page(user, auth_manager)

    elif st.session_state.page == "leaderboard":
        render_leaderboard_page(user, auth_manager)

    elif st.session_state.page == "public_profile":
        render_public_profile_page(user, auth_manager)


if __name__ == "__main__":
    main()

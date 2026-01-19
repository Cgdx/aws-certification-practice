import sqlite3
import json
import os
from typing import List, Optional
from datetime import datetime, timedelta
from .models import Question, ExamSession


class DatabaseManager:
    def __init__(self, db_path: str = "data/questions.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_database(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_type TEXT NOT NULL,
                domain TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                reference TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_type TEXT NOT NULL,
                date DATETIME NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                time_spent INTEGER NOT NULL,
                weak_domains TEXT
            )
        ''')

        # Spaced repetition table - now with user_id for per-user tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                user_id INTEGER DEFAULT 1,
                times_seen INTEGER DEFAULT 0,
                times_correct INTEGER DEFAULT 0,
                last_seen DATETIME,
                ease_factor REAL DEFAULT 2.5,
                interval_days INTEGER DEFAULT 1,
                next_review DATETIME,
                FOREIGN KEY (question_id) REFERENCES questions(id),
                UNIQUE(question_id, user_id)
            )
        ''')

        # Add user_id column to question_stats if not exists
        cursor.execute("PRAGMA table_info(question_stats)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in columns:
            cursor.execute('ALTER TABLE question_stats ADD COLUMN user_id INTEGER DEFAULT 1')

        # Add user_id column to exam_sessions if not exists
        cursor.execute("PRAGMA table_info(exam_sessions)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in columns:
            cursor.execute('ALTER TABLE exam_sessions ADD COLUMN user_id INTEGER DEFAULT 1')

        conn.commit()
        conn.close()

    def add_question(self, question: Question) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO questions (exam_type, domain, difficulty, question_text,
                                   options, correct_answer, explanation, reference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            question.exam_type,
            question.domain,
            question.difficulty,
            question.question_text,
            json.dumps(question.options),
            question.correct_answer,
            question.explanation,
            question.reference
        ))

        question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return question_id

    def get_questions_by_exam(self, exam_type: str, limit: Optional[int] = None) -> List[Question]:
        conn = self._get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT * FROM questions
            WHERE exam_type = ?
            ORDER BY difficulty ASC, RANDOM()
        '''
        if limit:
            query += f' LIMIT {limit}'

        cursor.execute(query, (exam_type,))
        rows = cursor.fetchall()
        conn.close()

        return [Question.from_dict(dict(row)) for row in rows]

    def get_questions_by_difficulty(self, exam_type: str, num_easy: int,
                                     num_medium: int, num_hard: int) -> List[Question]:
        conn = self._get_connection()
        cursor = conn.cursor()

        questions = []

        for difficulty, count in [(1, num_easy), (2, num_medium), (3, num_hard)]:
            cursor.execute('''
                SELECT * FROM questions
                WHERE exam_type = ? AND difficulty = ?
                ORDER BY RANDOM()
                LIMIT ?
            ''', (exam_type, difficulty, count))
            rows = cursor.fetchall()
            questions.extend([Question.from_dict(dict(row)) for row in rows])

        conn.close()
        return questions

    def get_all_questions(self, exam_type: str) -> List[Question]:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM questions
            WHERE exam_type = ?
            ORDER BY difficulty ASC
        ''', (exam_type,))
        rows = cursor.fetchall()
        conn.close()

        return [Question.from_dict(dict(row)) for row in rows]

    def get_question_count(self, exam_type: str) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM questions WHERE exam_type = ?', (exam_type,))
        count = cursor.fetchone()[0]
        conn.close()

        return count

    def save_exam_session(self, session: ExamSession, user_id: int = 1) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO exam_sessions (exam_type, date, score, total, time_spent, weak_domains, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session.exam_type,
            session.date.isoformat(),
            session.score,
            session.total,
            session.time_spent,
            json.dumps(session.weak_domains),
            user_id
        ))

        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def get_exam_sessions(self, exam_type: str, limit: int = 10, user_id: int = 1) -> List[ExamSession]:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM exam_sessions
            WHERE exam_type = ? AND user_id = ?
            ORDER BY date DESC
            LIMIT ?
        ''', (exam_type, user_id, limit))
        rows = cursor.fetchall()
        conn.close()

        return [ExamSession.from_dict(dict(row)) for row in rows]

    def import_questions_from_json(self, json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for q_data in data.get('questions', []):
            question = Question.from_dict(q_data)
            self.add_question(question)

    def clear_questions(self, exam_type: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM questions WHERE exam_type = ?', (exam_type,))
        conn.commit()
        conn.close()

    # Spaced Repetition Methods

    def update_question_stats(self, question_id: int, was_correct: bool, rating: int, user_id: int = 1):
        """
        Update question statistics after answering.

        rating: 1 = Again (review soon), 2 = Hard, 3 = Good, 4 = Easy
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get or create stats for this question and user
        cursor.execute('SELECT * FROM question_stats WHERE question_id = ? AND user_id = ?', (question_id, user_id))
        row = cursor.fetchone()

        now = datetime.now()

        if row:
            stats = dict(row)
            times_seen = stats['times_seen'] + 1
            times_correct = stats['times_correct'] + (1 if was_correct else 0)
            ease_factor = stats['ease_factor']
            interval = stats['interval_days']

            # SM-2 algorithm adaptation
            if was_correct:
                if rating == 4:  # Easy
                    ease_factor = min(ease_factor + 0.15, 3.0)
                    interval = int(interval * ease_factor * 1.3)
                elif rating == 3:  # Good
                    interval = int(interval * ease_factor)
                elif rating == 2:  # Hard
                    ease_factor = max(ease_factor - 0.15, 1.3)
                    interval = int(interval * 1.2)
            else:
                # Incorrect - reset interval
                if rating == 1:  # Again
                    interval = 1
                    ease_factor = max(ease_factor - 0.2, 1.3)
                else:
                    interval = max(1, interval // 2)
                    ease_factor = max(ease_factor - 0.1, 1.3)

            # Cap interval at 365 days
            interval = min(interval, 365)

            next_review = now + timedelta(days=interval)

            cursor.execute('''
                UPDATE question_stats
                SET times_seen = ?, times_correct = ?, last_seen = ?,
                    ease_factor = ?, interval_days = ?, next_review = ?
                WHERE question_id = ? AND user_id = ?
            ''', (times_seen, times_correct, now.isoformat(), ease_factor,
                  interval, next_review.isoformat(), question_id, user_id))
        else:
            # First time seeing this question
            if was_correct:
                interval = 1 if rating <= 2 else (4 if rating == 3 else 7)
            else:
                interval = 1

            next_review = now + timedelta(days=interval)

            cursor.execute('''
                INSERT INTO question_stats
                (question_id, user_id, times_seen, times_correct, last_seen, ease_factor, interval_days, next_review)
                VALUES (?, ?, 1, ?, ?, 2.5, ?, ?)
            ''', (question_id, user_id, 1 if was_correct else 0, now.isoformat(),
                  interval, next_review.isoformat()))

        conn.commit()
        conn.close()

    def get_questions_for_review(self, exam_type: str, limit: int = 65, user_id: int = 1) -> List[Question]:
        """
        Get questions prioritized by spaced repetition algorithm.
        Questions due for review come first, then new questions.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        # Get questions due for review (past their next_review date) for this user
        cursor.execute('''
            SELECT q.* FROM questions q
            LEFT JOIN question_stats qs ON q.id = qs.question_id AND qs.user_id = ?
            WHERE q.exam_type = ?
            AND (qs.next_review IS NULL OR qs.next_review <= ?)
            ORDER BY
                CASE WHEN qs.next_review IS NULL THEN 1 ELSE 0 END,
                qs.next_review ASC,
                qs.ease_factor ASC,
                RANDOM()
            LIMIT ?
        ''', (user_id, exam_type, now, limit))

        rows = cursor.fetchall()
        questions = [Question.from_dict(dict(row)) for row in rows]

        # If not enough questions due, add random new ones
        if len(questions) < limit:
            existing_ids = [q.id for q in questions]
            placeholders = ','.join(['?' for _ in existing_ids]) if existing_ids else '0'

            cursor.execute(f'''
                SELECT q.* FROM questions q
                LEFT JOIN question_stats qs ON q.id = qs.question_id AND qs.user_id = ?
                WHERE q.exam_type = ?
                AND q.id NOT IN ({placeholders})
                ORDER BY
                    CASE WHEN qs.id IS NULL THEN 0 ELSE 1 END,
                    qs.times_seen ASC,
                    RANDOM()
                LIMIT ?
            ''', [user_id, exam_type] + existing_ids + [limit - len(questions)])

            rows = cursor.fetchall()
            questions.extend([Question.from_dict(dict(row)) for row in rows])

        conn.close()

        # Sort by difficulty for the exam
        questions.sort(key=lambda q: (q.difficulty, q.id))

        return questions[:limit]

    def get_question_stats(self, question_id: int, user_id: int = 1) -> Optional[dict]:
        """Get stats for a specific question and user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM question_stats WHERE question_id = ? AND user_id = ?', (question_id, user_id))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_learning_progress(self, exam_type: str, user_id: int = 1) -> dict:
        """Get overall learning progress statistics for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Total questions
        cursor.execute('SELECT COUNT(*) FROM questions WHERE exam_type = ?', (exam_type,))
        total = cursor.fetchone()[0]

        # Questions seen at least once by this user
        cursor.execute('''
            SELECT COUNT(DISTINCT qs.question_id)
            FROM question_stats qs
            JOIN questions q ON qs.question_id = q.id
            WHERE q.exam_type = ? AND qs.user_id = ?
        ''', (exam_type, user_id))
        seen = cursor.fetchone()[0]

        # Questions due for review for this user
        now = datetime.now().isoformat()
        cursor.execute('''
            SELECT COUNT(*)
            FROM question_stats qs
            JOIN questions q ON qs.question_id = q.id
            WHERE q.exam_type = ? AND qs.user_id = ? AND qs.next_review <= ?
        ''', (exam_type, user_id, now))
        due = cursor.fetchone()[0]

        # Questions mastered (interval > 21 days) for this user
        cursor.execute('''
            SELECT COUNT(*)
            FROM question_stats qs
            JOIN questions q ON qs.question_id = q.id
            WHERE q.exam_type = ? AND qs.user_id = ? AND qs.interval_days > 21
        ''', (exam_type, user_id))
        mastered = cursor.fetchone()[0]

        # Average success rate for this user
        cursor.execute('''
            SELECT AVG(CAST(qs.times_correct AS FLOAT) / NULLIF(qs.times_seen, 0))
            FROM question_stats qs
            JOIN questions q ON qs.question_id = q.id
            WHERE q.exam_type = ? AND qs.user_id = ? AND qs.times_seen > 0
        ''', (exam_type, user_id))
        avg_success = cursor.fetchone()[0] or 0

        conn.close()

        return {
            "total": total,
            "seen": seen,
            "new": total - seen,
            "due_for_review": due,
            "mastered": mastered,
            "avg_success_rate": avg_success * 100
        }

import sqlite3
import bcrypt
import re
import os
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any
from .models import User, Certification


class AuthManager:
    def __init__(self, db_path: str):
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

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password_hash TEXT,
                auth_provider TEXT DEFAULT 'email',
                created_at DATETIME NOT NULL,
                last_login DATETIME
            )
        ''')

        # Migration: Add new user profile columns
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [col[1] for col in cursor.fetchall()]

        if 'nickname' not in user_columns:
            cursor.execute('ALTER TABLE users ADD COLUMN nickname TEXT')
        if 'phone' not in user_columns:
            cursor.execute('ALTER TABLE users ADD COLUMN phone TEXT')
        if 'show_in_leaderboard' not in user_columns:
            cursor.execute('ALTER TABLE users ADD COLUMN show_in_leaderboard INTEGER DEFAULT 0')
        if 'experience' not in user_columns:
            cursor.execute('ALTER TABLE users ADD COLUMN experience INTEGER DEFAULT 0')
        if 'credly_url' not in user_columns:
            cursor.execute('ALTER TABLE users ADD COLUMN credly_url TEXT')

        # Certifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS certifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                issued_date DATETIME,
                expiry_date DATETIME,
                credential_id TEXT,
                credly_badge_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Add user_id column to existing tables if not exists
        # Check if user_id exists in question_stats
        cursor.execute("PRAGMA table_info(question_stats)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in columns:
            cursor.execute('ALTER TABLE question_stats ADD COLUMN user_id INTEGER DEFAULT 1')

        # Check if user_id exists in exam_sessions
        cursor.execute("PRAGMA table_info(exam_sessions)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'user_id' not in columns:
            cursor.execute('ALTER TABLE exam_sessions ADD COLUMN user_id INTEGER DEFAULT 1')

        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        return True, ""

    def register(self, email: str, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Register a new user with email and password.
        Returns: (success, message, user)
        """
        # Validate email
        if not self._validate_email(email):
            return False, "Invalid email format", None

        # Validate password
        valid, msg = self._validate_password(password)
        if not valid:
            return False, msg, None

        # Validate username
        if len(username) < 2:
            return False, "Username must be at least 2 characters", None

        conn = self._get_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email.lower(),))
        if cursor.fetchone():
            conn.close()
            return False, "Email already registered", None

        # Create user
        password_hash = self._hash_password(password)
        now = datetime.now()

        try:
            cursor.execute('''
                INSERT INTO users (email, username, password_hash, auth_provider, created_at, last_login)
                VALUES (?, ?, ?, 'email', ?, ?)
            ''', (email.lower(), username, password_hash, now.isoformat(), now.isoformat()))

            user_id = cursor.lastrowid
            conn.commit()

            user = User(
                id=user_id,
                email=email.lower(),
                username=username,
                password_hash=password_hash,
                auth_provider='email',
                created_at=now,
                last_login=now
            )

            conn.close()
            return True, "Registration successful", user

        except Exception as e:
            conn.close()
            return False, f"Registration failed: {str(e)}", None

    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Login with email and password.
        Returns: (success, message, user)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email.lower(),))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return False, "Email not found", None

        user_data = dict(row)

        # Check if this is an OAuth account
        if user_data['auth_provider'] != 'email':
            conn.close()
            return False, f"This account uses {user_data['auth_provider']} login", None

        # Verify password
        if not self._verify_password(password, user_data['password_hash']):
            conn.close()
            return False, "Incorrect password", None

        # Update last login
        now = datetime.now()
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?',
                      (now.isoformat(), user_data['id']))
        conn.commit()
        conn.close()

        user_data['last_login'] = now
        user = User.from_dict(user_data)

        return True, "Login successful", user

    def login_or_register_oauth(self, email: str, username: str, provider: str) -> Tuple[bool, str, Optional[User]]:
        """
        Login or register a user via OAuth (Google, etc.).
        Returns: (success, message, user)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email.lower(),))
        row = cursor.fetchone()

        now = datetime.now()

        if row:
            # Existing user - update last login
            user_data = dict(row)
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?',
                          (now.isoformat(), user_data['id']))
            conn.commit()

            user_data['last_login'] = now
            user = User.from_dict(user_data)
            conn.close()
            return True, "Login successful", user
        else:
            # New user - register
            try:
                cursor.execute('''
                    INSERT INTO users (email, username, password_hash, auth_provider, created_at, last_login)
                    VALUES (?, ?, NULL, ?, ?, ?)
                ''', (email.lower(), username, provider, now.isoformat(), now.isoformat()))

                user_id = cursor.lastrowid
                conn.commit()

                user = User(
                    id=user_id,
                    email=email.lower(),
                    username=username,
                    password_hash=None,
                    auth_provider=provider,
                    created_at=now,
                    last_login=now
                )

                conn.close()
                return True, "Registration successful", user

            except Exception as e:
                conn.close()
                return False, f"Registration failed: {str(e)}", None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User.from_dict(dict(row))
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email.lower(),))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User.from_dict(dict(row))
        return None

    def update_user_profile(self, user_id: int, nickname: Optional[str] = None,
                           phone: Optional[str] = None,
                           show_in_leaderboard: bool = False,
                           credly_url: Optional[str] = None) -> Tuple[bool, str]:
        """
        Update user profile information.
        Returns: (success, message)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE users
                SET nickname = ?, phone = ?, show_in_leaderboard = ?, credly_url = ?
                WHERE id = ?
            ''', (nickname, phone, 1 if show_in_leaderboard else 0, credly_url, user_id))

            conn.commit()
            conn.close()
            return True, "Profile updated successfully"

        except Exception as e:
            conn.close()
            return False, f"Failed to update profile: {str(e)}"

    def change_password(self, user_id: int, current_password: str,
                       new_password: str) -> Tuple[bool, str]:
        """
        Change user password (only for email auth users).
        Returns: (success, message)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get current user
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return False, "User not found"

        user_data = dict(row)

        # Check if this is an email account
        if user_data['auth_provider'] != 'email':
            conn.close()
            return False, "Password change is only available for email accounts"

        # Verify current password
        if not self._verify_password(current_password, user_data['password_hash']):
            conn.close()
            return False, "Current password is incorrect"

        # Validate new password
        valid, msg = self._validate_password(new_password)
        if not valid:
            conn.close()
            return False, msg

        # Hash and save new password
        new_hash = self._hash_password(new_password)

        try:
            cursor.execute('''
                UPDATE users SET password_hash = ? WHERE id = ?
            ''', (new_hash, user_id))

            conn.commit()
            conn.close()
            return True, "Password changed successfully"

        except Exception as e:
            conn.close()
            return False, f"Failed to change password: {str(e)}"

    def get_leaderboard_users(self, weekly: bool = False) -> List[Dict[str, Any]]:
        """
        Get users who have opted in to the leaderboard, along with their exam stats.
        Returns list of dicts with user info and statistics.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Date filter for weekly
        date_filter = ""
        if weekly:
            date_filter = "AND es.date >= datetime('now', '-7 days')"

        # Get users who opted in to leaderboard with their exam statistics
        cursor.execute(f'''
            SELECT
                u.id,
                u.username,
                u.nickname,
                u.experience,
                COUNT(es.id) as exams_taken,
                AVG(CAST(es.score AS FLOAT) / es.total * 100) as avg_score,
                MAX(CAST(es.score AS FLOAT) / es.total * 100) as best_score
            FROM users u
            LEFT JOIN exam_sessions es ON u.id = es.user_id {date_filter}
            WHERE u.show_in_leaderboard = 1
            GROUP BY u.id
            HAVING exams_taken > 0
            ORDER BY u.experience DESC, avg_score DESC, best_score DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        leaderboard = []
        for rank, row in enumerate(rows, 1):
            row_dict = dict(row)
            leaderboard.append({
                'rank': rank,
                'user_id': row_dict['id'],
                'display_name': row_dict['nickname'] or row_dict['username'],
                'exams_taken': row_dict['exams_taken'],
                'avg_score': row_dict['avg_score'] or 0,
                'best_score': row_dict['best_score'] or 0,
                'experience': row_dict['experience'] or 0
            })

        return leaderboard

    def add_experience(self, user_id: int, points: int) -> Tuple[bool, int]:
        """
        Add experience points to a user.
        Returns: (success, new_total_experience)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE users SET experience = COALESCE(experience, 0) + ? WHERE id = ?
            ''', (points, user_id))

            cursor.execute('SELECT experience FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            new_exp = row['experience'] if row else 0

            conn.commit()
            conn.close()
            return True, new_exp

        except Exception as e:
            conn.close()
            return False, 0

    def get_user_certifications(self, user_id: int) -> List[Certification]:
        """Get all certifications for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM certifications WHERE user_id = ? ORDER BY issued_date DESC
        ''', (user_id,))

        rows = cursor.fetchall()
        conn.close()

        return [Certification.from_dict(dict(row)) for row in rows]

    def add_certification(self, user_id: int, name: str, code: str,
                         issued_date: Optional[datetime] = None,
                         expiry_date: Optional[datetime] = None,
                         credential_id: Optional[str] = None,
                         credly_badge_url: Optional[str] = None) -> Tuple[bool, str]:
        """Add a certification to a user's profile."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO certifications (user_id, name, code, issued_date, expiry_date, credential_id, credly_badge_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, name, code,
                  issued_date.isoformat() if issued_date else None,
                  expiry_date.isoformat() if expiry_date else None,
                  credential_id, credly_badge_url))

            conn.commit()
            conn.close()
            return True, "Certification added successfully"

        except Exception as e:
            conn.close()
            return False, f"Failed to add certification: {str(e)}"

    def delete_certification(self, cert_id: int, user_id: int) -> Tuple[bool, str]:
        """Delete a certification (only if owned by user)."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                DELETE FROM certifications WHERE id = ? AND user_id = ?
            ''', (cert_id, user_id))

            conn.commit()
            conn.close()
            return True, "Certification deleted"

        except Exception as e:
            conn.close()
            return False, f"Failed to delete certification: {str(e)}"

    def get_public_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get public profile data for a user."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                u.id,
                u.username,
                u.nickname,
                u.experience,
                u.credly_url,
                u.show_in_leaderboard,
                u.created_at,
                COUNT(es.id) as exams_taken,
                AVG(CAST(es.score AS FLOAT) / es.total * 100) as avg_score,
                MAX(CAST(es.score AS FLOAT) / es.total * 100) as best_score
            FROM users u
            LEFT JOIN exam_sessions es ON u.id = es.user_id
            WHERE u.id = ?
            GROUP BY u.id
        ''', (user_id,))

        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        row_dict = dict(row)

        # Get certifications
        cursor.execute('''
            SELECT * FROM certifications WHERE user_id = ? ORDER BY issued_date DESC
        ''', (user_id,))

        cert_rows = cursor.fetchall()
        certifications = [Certification.from_dict(dict(r)) for r in cert_rows]

        conn.close()

        # Only return if user opted into leaderboard
        if not row_dict.get('show_in_leaderboard'):
            return None

        return {
            'user_id': row_dict['id'],
            'display_name': row_dict['nickname'] or row_dict['username'],
            'experience': row_dict['experience'] or 0,
            'credly_url': row_dict['credly_url'],
            'member_since': row_dict['created_at'],
            'exams_taken': row_dict['exams_taken'] or 0,
            'avg_score': row_dict['avg_score'] or 0,
            'best_score': row_dict['best_score'] or 0,
            'certifications': certifications
        }

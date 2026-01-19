import sqlite3
import bcrypt
import re
import os
from datetime import datetime
from typing import Optional, Tuple
from .models import User


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

# pypilot/memory/chat_store.py

from pathlib import Path
from typing import Optional
import sqlite3


class DataBaseStore:
    def __init__(self):
        self.db_path = Path.home() / ".pypilot" / "chat.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.create_db()

    def create_db(self) -> bool:
        sql_statements = [
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                consent_given INTEGER NOT NULL DEFAULT 0,
                project_path TEXT NOT NULL UNIQUE,
                date TEXT DEFAULT CURRENT_DATE,
                time TEXT DEFAULT CURRENT_TIME
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS conversation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                provider TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                date TEXT DEFAULT CURRENT_DATE,
                time TEXT DEFAULT CURRENT_TIME,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            );
            """
        ]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cursor = conn.cursor()
                for statement in sql_statements:
                    cursor.execute(statement)
                conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print("Error:", e)
            return False

    def get_or_create_project(self, project_path: str) -> Optional[int]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cur = conn.cursor()
                cur.execute("SELECT project_id FROM projects WHERE project_path = ?", (project_path,))
                row = cur.fetchone()
                if row:
                    return row[0]
                cur.execute("INSERT INTO projects(project_path) VALUES(?)", (project_path,))
                conn.commit()
                return cur.lastrowid
        except sqlite3.OperationalError as e:
            print("Error:", e)
            return None

    def get_consent(self, project_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT consent_given FROM projects WHERE project_id = ?", (project_id,))
                row = cursor.fetchone()
                if row:
                    return bool(row[0])
        except sqlite3.OperationalError as e:
            print("Error:", e)
        return False

    def update_consent(self, project_id: int, consent: bool) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE projects SET consent_given = ? WHERE project_id = ?",
                    (int(consent), project_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except sqlite3.OperationalError as e:
            print("Error:", e)
            return False

    def fetch_id(self, project_path: str) -> Optional[int]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT project_id FROM projects WHERE project_path = ?", (project_path,))
                row = cursor.fetchone()
                return row[0] if row else None
        except sqlite3.OperationalError as e:
            print("Error:", e)
            return None

    def fetch_convo(self, project_id: int, limit: int = 5) -> Optional[list]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT question, answer FROM conversation WHERE project_id = ? ORDER BY id DESC LIMIT ?",
                    (project_id, limit)
                )
                return list(reversed(cur.fetchall()))
        except sqlite3.OperationalError as e:
            print("Error:", e)
            return None

    def insert_convo(self, project_id: int, provider: str, question: str, answer: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO conversation(project_id, provider, question, answer) VALUES(?, ?, ?, ?)",
                    (project_id, provider, question, answer)
                )
                conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print("Error:", e)
            return False

    def fetch_last_project_path(self) -> Optional[str]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT project_path FROM projects ORDER BY project_id DESC LIMIT 1")
                row = cursor.fetchone()
                return row[0] if row else None
        except sqlite3.OperationalError as e:
            print("Error:", e)
            return None
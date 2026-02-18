from pathlib import Path
from typing import Optional
import sqlite3


class DataBaseStore:
    def __init__(self, project_path: Path):
        self.db_path = project_path / ".pypilot" / "chat.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def create_db(self) -> bool:
        sql_statements = [
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            with sqlite3.connect(self.db_path) as connection:
                connection.execute("PRAGMA foreign_keys = ON;")
                cursor = connection.cursor()
                for statement in sql_statements:
                    cursor.execute(statement)
                connection.commit()
            return True

        except sqlite3.OperationalError as e:
            print("Error:", e)
            return False

    def insert_project(self, proj_path: str) -> Optional[int]:
        sql_project = """
            INSERT INTO projects(project_path)
            VALUES(?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cur = conn.cursor()
                cur.execute(sql_project, (proj_path,))
                conn.commit()
                return cur.lastrowid

        except sqlite3.OperationalError as e:
            print("Error:", e)
            return None

    def insert_convo(
        self,
        project_id: int,
        provider: str,
        question: str,
        answer: str
    ) -> bool:

        sql_chat = """
            INSERT INTO conversation(project_id, provider, question, answer)
            VALUES(?, ?, ?, ?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cur = conn.cursor()
                cur.execute(sql_chat, (project_id, provider, question, answer))
                conn.commit()
            return True

        except sqlite3.OperationalError as e:
            print("Error:", e)
            return False
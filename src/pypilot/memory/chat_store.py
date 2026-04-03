#pypilot/memorry/chat_store.py

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
            connection.close()
            print("Error:", e)

        connection.close()
        return False

    def get_or_create_project(self, project_path: str) -> Optional[int]:
        select_sql = """
            SELECT project_id FROM projects WHERE project_path = ?
        """

        insert_sql = """
            INSERT INTO projects(project_path) VALUES(?)
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cur = conn.cursor()
                cur.execute(select_sql, (project_path,))
                row = cur.fetchone()

                if row:
                    return row[0]

                cur.execute(insert_sql, (project_path,))
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
        
        conn.close()
        return False

    def fetch_id(self, project_path: str) -> Optional[int]:
        fetching_id = """
            SELECT project_id FROM projects WHERE project_path = ?
        """

        try:
            with sqlite3.connect(self.db_path) as connect:
                connect.execute("PRAGMA foreign_keys = ON;")
                cursor = connect.cursor()
                cursor.execute(fetching_id, (project_path,))
                id = cursor.fetchone()
            return id[0] if id else None
            
        except sqlite3.OperationalError as e:
            print("Error", e)

        connect.close()
        return None

    def fetch_convo(
            self,
            project_id: int,
            limit: int = 5
        ) -> Optional[list]:

        history = """
            SELECT question, answer 
            FROM conversation 
            WHERE project_id = ? 
            ORDER BY id DESC 
            LIMIT ?
        """

        try:
            with sqlite3.connect(self.db_path) as connect:
                cur = connect.cursor()
                cur.execute(history, (project_id, limit))
                convo = cur.fetchall()

            return list(reversed(convo))
        
        except sqlite3.OperationalError as e:
            print("Error :", e)

        connect.close()
        return None
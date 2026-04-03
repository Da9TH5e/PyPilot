<<<<<<< HEAD
#pypilot/memorry/chat_store.py

=======
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
from pathlib import Path
from typing import Optional
import sqlite3


class DataBaseStore:
<<<<<<< HEAD
    def __init__(self):
        self.db_path = Path.home() / ".pypilot" / "chat.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.create_db()
=======
    def __init__(self, project_path: Path):
        self.db_path = project_path / ".pypilot" / "chat.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4

    def create_db(self) -> bool:
        sql_statements = [
            """
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
<<<<<<< HEAD
                consent_given INTEGER NOT NULL DEFAULT 0,
=======
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
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
<<<<<<< HEAD
            with sqlite3.connect(self.db_path) as connect:
                connect.execute("PRAGMA foreign_keys = ON;")
                cursor = connect.cursor()
                for statement in sql_statements:
                    cursor.execute(statement)
                connect.commit()
            return True

        except sqlite3.OperationalError as e:
            connect.close()
            print("Error:", e)

        connect.close()
        return False

    def get_or_create_project(self, project_path: str) -> Optional[int]:
        select_sql = """
            SELECT project_id FROM projects WHERE project_path = ?
        """

        insert_sql = """
            INSERT INTO projects(project_path) VALUES(?)
        """

        try:
            with sqlite3.connect(self.db_path) as connect:
                connect.execute("PRAGMA foreign_keys = ON;")
                cur = connect.cursor()
                cur.execute(select_sql, (project_path,))
                row = cur.fetchone()

                if row:
                    return row[0]

                cur.execute(insert_sql, (project_path,))
                connect.commit()
=======
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
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
                return cur.lastrowid

        except sqlite3.OperationalError as e:
            print("Error:", e)
<<<<<<< HEAD

        return None
=======
            return None
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4

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
<<<<<<< HEAD
            with sqlite3.connect(self.db_path) as connect:
                connect.execute("PRAGMA foreign_keys = ON;")
                cur = connect.cursor()
                cur.execute(sql_chat, (project_id, provider, question, answer))
                connect.commit()
=======
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")
                cur = conn.cursor()
                cur.execute(sql_chat, (project_id, provider, question, answer))
                conn.commit()
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4
            return True

        except sqlite3.OperationalError as e:
            print("Error:", e)
<<<<<<< HEAD
        
        connect.close()
        return False
    
    def get_consent(self, project_id: int) -> bool:
        sql = "SELECT consent_given FROM projects WHERE project_id = ?"

        try:
            with sqlite3.connect(self.db_path) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, (project_id,))
                row = cursor.fetchone()
                if row:
                    return bool(row[0])
        except sqlite3.OperationalError as e:
            print("Error :", e)

        return False
    
    def update_consent(
            self,
            project_id: int,
            consent: bool,
        ) -> bool:

        sql = """
            UPDATE projects
            SET consent_given = ?
            WHERE project_id = ?
        """
        try:
            with sqlite3.connect(self.db_path) as connect:
                connect.execute("PRAGMA foreign_keys = ON;")
                cursor = connect.cursor()
                cursor.execute(sql, (int(consent), project_id))
                connect.commit()

                if cursor.rowcount == 0:
                    print("Warning: No project row updated.")
                    return False
                return True

        except sqlite3.OperationalError as e:
            print("Error :", e)
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
    
    def fetch_last_project_path(self) -> Optional[str]:
        sql = """
            SELECT project_path from projects
            ORDER BY project_id 
            DESC LIMIT 1
        """

        try:
            with sqlite3.connect(self.db_path) as connect:
                cursor = connect.cursor()
                cursor.execute(sql)
                row = cursor.fetchone()

                return row[0] if row else None
            
        except sqlite3.OperationalError as e:
            print("Error :", e)

        connect.close()
        return None
=======
            return False
>>>>>>> 415efd0dba29b694494a84f60f1afd4662135ff4

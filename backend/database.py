import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/educational_ai.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            file_name TEXT,

            summary TEXT,

            quiz TEXT,

            flashcards TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT

)
""")

        self.connection.commit()

    def save_history(self, file_name, summary, quiz, flashcards):

        self.cursor.execute("""

        INSERT INTO history
        (file_name,summary,quiz,flashcards)

        VALUES(?,?,?,?)

        """,

        (
            file_name,
            summary,
            quiz,
            flashcards
        ))

        self.connection.commit()

    def get_history(self):

        self.cursor.execute("""

        SELECT * FROM history
        ORDER BY id DESC

        """)

        return self.cursor.fetchall()
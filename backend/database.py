import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/educational_ai.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    # --------------------------------------------------
    # CREATE TABLES
    # --------------------------------------------------

    def create_tables(self):

        # History table
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

        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE,

                password TEXT

            )
        """)

        # Study Plans table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_plans(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT,

                subjects TEXT,

                exam_date TEXT,

                study_hours INTEGER,

                plan TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # Quiz Scores table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_scores(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT,

                subject TEXT,

                score INTEGER,

                total INTEGER,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        self.connection.commit()

    # --------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------

    def save_history(
        self,
        file_name,
        summary,
        quiz,
        flashcards
    ):

        self.cursor.execute("""
            INSERT INTO history
            (
                file_name,
                summary,
                quiz,
                flashcards
            )

            VALUES (?, ?, ?, ?)
        """,
        (
            file_name,
            summary,
            quiz,
            flashcards
        ))

        self.connection.commit()

    # --------------------------------------------------
    # GET HISTORY
    # --------------------------------------------------

    def get_history(self):

        self.cursor.execute("""
            SELECT *
            FROM history
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    # --------------------------------------------------
    # SAVE STUDY PLAN
    # --------------------------------------------------

    def save_study_plan(
        self,
        username,
        subjects,
        exam_date,
        study_hours,
        plan
    ):

        self.cursor.execute("""
            INSERT INTO study_plans
            (
                username,
                subjects,
                exam_date,
                study_hours,
                plan
            )

            VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            subjects,
            str(exam_date),
            study_hours,
            plan
        ))

        self.connection.commit()

    # --------------------------------------------------
    # GET STUDY PLANS
    # --------------------------------------------------

    def get_study_plans(self, username):

        self.cursor.execute("""
            SELECT *
            FROM study_plans
            WHERE username = ?
            ORDER BY created_at DESC
        """,
        (username,))

        return self.cursor.fetchall()

    # --------------------------------------------------
    # SAVE QUIZ SCORE
    # --------------------------------------------------

    def save_quiz_score(
        self,
        username,
        subject,
        score,
        total
    ):

        self.cursor.execute("""
            INSERT INTO quiz_scores
            (
                username,
                subject,
                score,
                total
            )

            VALUES (?, ?, ?, ?)
        """,
        (
            username,
            subject,
            score,
            total
        ))

        self.connection.commit()

    # --------------------------------------------------
    # GET QUIZ SCORES
    # --------------------------------------------------

    def get_quiz_scores(self, username):

        self.cursor.execute("""
            SELECT *
            FROM quiz_scores
            WHERE username = ?
            ORDER BY created_at DESC
        """,
        (username,))

        return self.cursor.fetchall()
from backend.database import Database


class DashboardService:

    def __init__(self):

        self.db = Database()

    def statistics(self):

        history = self.db.get_history()

        stats = {
            "files": len(history),
            "summaries": 0,
            "quizzes": 0,
            "flashcards": 0
        }

        for row in history:

            if row[2]:
                stats["summaries"] += 1

            if row[3]:
                stats["quizzes"] += 1

            if row[4]:
                stats["flashcards"] += 1

        return stats
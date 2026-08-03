from backend.rag.rag_service import RAGService
from backend.services.gemini_service import GeminiService


class ChatService:

    def __init__(self):

        self.rag = RAGService()

        self.gemini = GeminiService()

    def ask(self, vector_db, question):

        context = self.rag.search(
            vector_db,
            question
        )

        return self.gemini.ask_from_context(
            context,
            question
        )
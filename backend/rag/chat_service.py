from backend.rag.rag_service import RAGService
from backend.services.gemini_service import GeminiService


class ChatService:

    def __init__(self):

        self.rag = RAGService()
        self.gemini = GeminiService()

    def ask(self, vector_db, question):

        if not question or not question.strip():
            return "Please enter a question."

        # No PDF uploaded
        if vector_db is None:

            prompt = f"""
You are an intelligent educational AI tutor.

The student has not uploaded any PDF.

Answer the student's question using your general knowledge.
Do not mention any uploaded PDF.
Do not say that the information is missing from a PDF.

Give a clear, accurate and student-friendly explanation.

Student question:
{question}
"""

            return self.gemini.ask(prompt)

        # PDF is available
        context = self.rag.search(
            vector_db,
            question
        )

        # PDF exists but no useful context was found
        if not context or not context.strip():

            prompt = f"""
You are an intelligent educational AI tutor.

The student uploaded a PDF, but the uploaded document
does not contain useful information for this particular question.

Answer the question using your general knowledge.
Do not say that you could not find it in the PDF.

Give a clear, accurate and student-friendly explanation.

Student question:
{question}
"""

            return self.gemini.ask(prompt)

        # PDF contains relevant context
        return self.gemini.ask_from_context(
            context,
            question
        )
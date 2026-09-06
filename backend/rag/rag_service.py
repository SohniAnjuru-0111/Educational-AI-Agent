from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


class RAGService:

    def __init__(self):

        self.embedding = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

    def load_pdf(self, text):

        if not text or not text.strip():
            raise ValueError(
                "No text available to create embeddings."
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents([text])

        if not docs:
            raise ValueError(
                "No document chunks were created."
            )

        db = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding
        )

        return db

    def search(self, db, question):

        if db is None:
            return ""

        if not question or not question.strip():
            return ""

        docs = db.similarity_search(
            question,
            k=3
        )

        context = ""

        for doc in docs:
            context += doc.page_content
            context += "\n\n"

        return context
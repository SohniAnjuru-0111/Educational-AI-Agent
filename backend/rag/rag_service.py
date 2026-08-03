import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


class RAGService:

    def __init__(self):

        self.embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def load_pdf(self, text):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents([text])

        db = Chroma.from_documents(
    documents=docs,
    embedding=self.embedding
)
        return db

    def search(self, db, question):

        docs = db.similarity_search(
            question,
            k=3
        )

        context = ""

        for doc in docs:
            context += doc.page_content
            context += "\n\n"

        return context
import streamlit as st
import plotly.graph_objects as go

from backend.database import Database
from backend.auth.auth_service import AuthService

from backend.services.pdf_reader import PDFReader
from backend.services.summary_generator import SummaryGenerator
from backend.services.quiz_generator import QuizGenerator
from backend.services.flashcard_generator import FlashcardGenerator
from backend.services.pdf_export import PDFExporter
from backend.services.dashboard_service import DashboardService
from backend.services.quiz_evaluator import QuizEvaluator

from backend.rag.rag_service import RAGService
from backend.rag.chat_service import ChatService


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Educational AI Agent",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------

db = Database()
auth = AuthService()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if not st.session_state.logged_in:

    st.title("🎓 Educational AI Agent")

    st.subheader("Login / Register")

    option = st.selectbox(
        "Choose",
        [
            "Login",
            "Register"
        ]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if option == "Register":

        if st.button("Register"):

            if auth.register(username, password):

                st.success("Registration Successful")

            else:

                st.error("Username already exists")

    else:

        if st.button("Login"):

            if auth.login(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🎓 Educational AI Agent")

    st.success(f"Welcome\n\n{st.session_state.username}")

    st.markdown("---")

    st.write("### Features")

    st.write("📚 AI Summary")
    st.write("❓ AI Quiz")
    st.write("🧠 Flashcards")
    st.write("📝 Evaluation")
    st.write("📜 History")
    st.write("📊 Dashboard")
    st.write("💬 Chat with PDF")

    st.markdown("---")

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 Educational AI Agent")

st.write(
    "Upload your study PDF and generate AI-powered learning resources."
)

st.divider()

# --------------------------------------------------
# PDF UPLOADER
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📂 Upload PDF",
    type=["pdf"]
)

if uploaded_file is None:

    st.info("Please upload a PDF to continue.")

    st.stop()

# --------------------------------------------------
# READ PDF
# --------------------------------------------------

reader = PDFReader()

text = reader.extract_text(uploaded_file)

if not text.strip():

    st.error("No text found inside the PDF.")

    st.stop()

# --------------------------------------------------
# LOAD RAG DATABASE
# --------------------------------------------------

if not st.session_state.pdf_loaded:

    rag = RAGService()

    st.session_state.vector_db = rag.load_pdf(text)

    st.session_state.pdf_loaded = True

st.success("✅ PDF Uploaded Successfully")

st.subheader("📄 Uploaded PDF")

st.success(uploaded_file.name)

with st.expander("View Extracted Text"):

    st.write(text)

st.divider()

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📚 Summary",
        "❓ Quiz",
        "🧠 Flashcards",
        "📝 Evaluation",
        "📜 History",
        "📊 Dashboard",
        "💬 Chat"
    ]
)
# =====================================================
# SUMMARY TAB
# =====================================================

with tab1:

    st.subheader("📚 AI Summary")

    if st.button("Generate Summary"):

        with st.spinner("Generating Summary..."):

            summary = SummaryGenerator().generate_summary(text)

        db.save_history(
            uploaded_file.name,
            summary,
            "",
            ""
        )

        st.success("Summary Generated Successfully!")

        st.markdown(summary)

        pdf_path = PDFExporter().export(
            "AI Summary",
            summary,
            "summary.pdf"
        )

        with open(pdf_path, "rb") as file:

            st.download_button(
                "📥 Download Summary PDF",
                file,
                file_name="AI_Summary.pdf",
                mime="application/pdf"
            )
# =====================================================
# QUIZ TAB
# =====================================================

with tab2:

    st.subheader("❓ AI Quiz")

    if st.button("Generate Quiz"):

        with st.spinner("Generating Quiz..."):

            quiz = QuizGenerator().generate_quiz(text)

        db.save_history(
            uploaded_file.name,
            "",
            quiz,
            ""
        )

        st.success("Quiz Generated Successfully!")

        st.markdown(quiz)

        pdf_path = PDFExporter().export(
            "AI Quiz",
            quiz,
            "quiz.pdf"
        )

        with open(pdf_path, "rb") as file:

            st.download_button(
                "📥 Download Quiz PDF",
                file,
                file_name="AI_Quiz.pdf",
                mime="application/pdf"
            )
# =====================================================
# FLASHCARDS TAB
# =====================================================

with tab3:

    st.subheader("🧠 AI Flashcards")

    if st.button("Generate Flashcards"):

        with st.spinner("Generating Flashcards..."):

            flashcards = FlashcardGenerator().generate_flashcards(text)

        db.save_history(
            uploaded_file.name,
            "",
            "",
            flashcards
        )

        st.success("Flashcards Generated Successfully!")

        st.markdown(flashcards)

        pdf_path = PDFExporter().export(
            "AI Flashcards",
            flashcards,
            "flashcards.pdf"
        )

        with open(pdf_path, "rb") as file:

            st.download_button(
                "📥 Download Flashcards PDF",
                file,
                file_name="AI_Flashcards.pdf",
                mime="application/pdf"
            )
# =====================================================
# EVALUATION TAB
# =====================================================

with tab4:

    st.subheader("📝 Quiz Evaluation")

    quiz_text = st.text_area(
        "Paste Generated Quiz",
        height=250
    )

    student_answers = st.text_area(
        "Enter Your Answers",
        height=200
    )

    if st.button("Evaluate Quiz"):

        with st.spinner("Evaluating..."):

            result = QuizEvaluator().evaluate(
                quiz_text,
                student_answers
            )

        st.success("Evaluation Complete!")

        st.markdown(result)
# =====================================================
# HISTORY TAB
# =====================================================

with tab5:

    st.subheader("📜 Study History")

    history = db.get_history()

    if len(history) == 0:

        st.info("No study history available.")

    else:

        for row in history:

            with st.expander(f"📄 {row[1]} | {row[5]}"):

                if row[2]:
                    st.markdown("### 📚 Summary")
                    st.write(row[2])

                if row[3]:
                    st.markdown("### ❓ Quiz")
                    st.write(row[3])

                if row[4]:
                    st.markdown("### 🧠 Flashcards")
                    st.write(row[4])
# =====================================================
# DASHBOARD TAB
# =====================================================

with tab6:

    st.subheader("📊 Dashboard")

    stats = DashboardService().statistics()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📄 PDFs Processed",
            stats["files"]
        )

        st.metric(
            "📚 Summaries",
            stats["summaries"]
        )

    with col2:

        st.metric(
            "❓ Quizzes",
            stats["quizzes"]
        )

        st.metric(
            "🧠 Flashcards",
            stats["flashcards"]
        )

    fig = go.Figure()

    fig.add_bar(
        x=[
            "Summaries",
            "Quizzes",
            "Flashcards"
        ],
        y=[
            stats["summaries"],
            stats["quizzes"],
            stats["flashcards"]
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
)
# =====================================================
# CHAT WITH PDF
# =====================================================

with tab7:

    st.subheader("💬 Chat with Uploaded PDF")

    question = st.text_input(
        "Ask any question about the uploaded PDF"
    )

    if st.button("Ask AI"):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching document..."):

                answer = ChatService().ask(
                    st.session_state.vector_db,
                    question
                )

            st.session_state.chat_history.append(
                ("You", question)
            )

            st.session_state.chat_history.append(
                ("AI", answer)
            )

    st.markdown("---")

    if len(st.session_state.chat_history) == 0:

        st.info("Ask a question about the uploaded PDF.")

    else:

        for speaker, message in st.session_state.chat_history:

            if speaker == "You":

                with st.chat_message("user"):

                    st.write(message)

            else:

                with st.chat_message("assistant"):

                    st.write(message)
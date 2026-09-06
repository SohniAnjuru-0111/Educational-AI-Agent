import streamlit as st
import plotly.graph_objects as go
import base64
from pathlib import Path

from backend.database import Database
from backend.auth.auth_service import AuthService

from backend.services.pdf_reader import PDFReader
from backend.services.summary_generator import SummaryGenerator
from backend.services.quiz_generator import QuizGenerator
from backend.services.flashcard_generator import FlashcardGenerator
from backend.services.pdf_export import PDFExporter
from backend.services.dashboard_service import DashboardService
from backend.services.quiz_evaluator import QuizEvaluator
from backend.services.study_planner import StudyPlanner
from backend.services.voice_service import VoiceService
from backend.services.tts_service import TTSService
from backend.services.gemini_service import GeminiService

import plotly.graph_objects as go
from backend.rag.rag_service import RAGService
from backend.rag.chat_service import ChatService

with open("styles.css", "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
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

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""
# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if not st.session_state.logged_in:

    # ==============================
    # LOGIN PAGE BACKGROUND
    # ==============================

    bg_path = Path("assets/login_background.png")

    if bg_path.exists():

        bg_base64 = base64.b64encode(
            bg_path.read_bytes()
        ).decode()

        st.markdown(
            f"""
<style>

/* LOGIN PAGE BACKGROUND ONLY */

.stApp {{
    background-image: url(
        "data:image/png;base64,{bg_base64}"
    ) !important;

    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
    min-height: 100vh !important;
}}

/* Make Streamlit containers transparent */

[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
section.main,
.main,
.block-container {{
    background: transparent !important;
}}

/* Remove unnecessary top spacing */

.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
}}

/* ==============================
   LOGIN FOOTER FIX
   ============================== */

.login-footer {{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 18px;
    margin: 28px auto 0 auto;
    padding: 12px 20px;
    box-sizing: border-box;
    text-align: center;
}}

.login-footer span {{
    color: #64748b !important;
    font-size: 15px;
    font-weight: 500;
    white-space: nowrap;
}}

.login-footer .footer-dot {{
    color: #6366f1 !important;
    font-size: 18px;
    font-weight: 700;
}}

@media (max-width: 800px) {{
    .login-footer {{
        gap: 10px;
        flex-wrap: wrap;
    }}

    .login-footer span {{
        font-size: 13px;
    }}
}}

</style>
""",
            unsafe_allow_html=True
        )

    # ==============================
    # LOGIN HERO
    # ==============================

    st.markdown(
        '<div class="login-hero">'
        '<div class="login-logo">🎓</div>'
        '<div class="login-title">EduAI</div>'
        '<div class="login-subtitle">'
        'Your Personal AI Learning Assistant'
        '</div>'
        '<div class="login-description">'
        'Learn smarter. Practice better. Achieve more.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ==============================
    # LOGIN FORM
    # ==============================

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        with st.container(key="login_card"):

            option = st.radio(
                "Account",
                ["Login", "Register"],
                horizontal=True,
                label_visibility="collapsed",
                key="auth_option"
            )

            st.markdown(
                '<div class="login-space"></div>',
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="auth_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="auth_password"
            )

            st.markdown(
                '<div class="login-space-small"></div>',
                unsafe_allow_html=True
            )

            # ==============================
            # REGISTER
            # ==============================

            if option == "Register":

                if st.button(
                    "✨ Create Account",
                    use_container_width=True,
                    key="register_button"
                ):

                    if not username.strip() or not password.strip():

                        st.warning(
                            "Please enter both username and password."
                        )

                    elif auth.register(username, password):

                        st.success(
                            "🎉 Registration successful! "
                            "You can now login."
                        )

                    else:

                        st.error(
                            "❌ Username already exists."
                        )

            # ==============================
            # LOGIN
            # ==============================

            else:

                if st.button(
                    "🚀 Login to EduAI",
                    use_container_width=True,
                    key="login_button"
                ):

                    if not username.strip() or not password.strip():

                        st.warning(
                            "Please enter your username and password."
                        )

                    elif auth.login(username, password):

                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.current_page = "Dashboard"

                        st.rerun()

                    else:

                        st.error(
                            "❌ Invalid username or password."
                        )

    # ==============================
    # LOGIN FOOTER
    # ==============================

    st.markdown(
        """
        <div class="login-footer">
            <span>📚 AI-Powered Learning</span>
            <span class="footer-dot">•</span>
            <span>🧠 Personalized Study</span>
            <span class="footer-dot">•</span>
            <span>🎯 Better Results</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()
# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🎓 EduAI")

    st.success(
        f"Welcome\n\n{st.session_state.username}"
    )

    st.markdown("---")

    st.subheader("Navigation")

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.session_state.current_page = "Dashboard"
        st.rerun()

    if st.button(
        "📚 AI Summary",
        use_container_width=True
    ):
        st.session_state.current_page = "AI Summary"
        st.rerun()

    if st.button(
        "❓ AI Quiz",
        use_container_width=True
    ):
        st.session_state.current_page = "AI Quiz"
        st.rerun()

    if st.button(
        "🧠 Flashcards",
        use_container_width=True
    ):
        st.session_state.current_page = "Flashcards"
        st.rerun()

    if st.button(
        "📝 Evaluation",
        use_container_width=True
    ):
        st.session_state.current_page = "Evaluation"
        st.rerun()

    if st.button(
        "💬 AI Tutor",
        use_container_width=True
    ):
        st.session_state.current_page = "AI Tutor"
        st.rerun()

    if st.button(
        "📅 Study Planner",
        use_container_width=True
    ):
        st.session_state.current_page = "Study Planner"
        st.rerun()

    if st.button(
        "📊 Progress",
        use_container_width=True
    ):
        st.session_state.current_page = "Progress"
        st.rerun()

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()


# --------------------------------------------------
# AI TUTOR
# --------------------------------------------------

if st.session_state.current_page == "AI Tutor":

    st.subheader("💬 AI Tutor")

    st.write(
        "Ask anything — with or without an uploaded PDF."
    )

    # --------------------------------------------------
    # TEXT AI TUTOR
    # --------------------------------------------------

    st.markdown("### 💬 Ask AI")

    question = st.text_input(
        "Type your question",
        key="tutor_question"
    )

    if st.button(
        "🤖 Ask AI",
        key="tutor_ask"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "🤖 AI Tutor is thinking..."
            ):

                try:

                    if st.session_state.get(
                        "pdf_loaded",
                        False
                    ):

                        answer = ChatService().ask(
                            st.session_state.vector_db,
                            question
                        )

                    else:

                        answer = GeminiService().ask(
                            question
                        )

                    st.session_state.chat_history.append(
                        ("You", question)
                    )

                    st.session_state.chat_history.append(
                        ("AI", answer)
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Unable to answer: {e}"
                    )

    # --------------------------------------------------
    # VOICE TUTOR
    # --------------------------------------------------

    st.markdown("---")

    st.markdown("### 🎤 Voice Tutor")

    st.write(
        "Ask your question using your microphone."
    )

    try:

        voice_service = VoiceService()

        voice_context = voice_service.start_recording()

        if st.button(
            "📝 Convert Voice to Text",
            key="convert_voice_tutor"
        ):

            spoken_text = voice_service.convert_to_text(
                voice_context
            )

            if spoken_text:

                st.session_state.voice_question = spoken_text

                st.success(
                    f"🎤 You said: {spoken_text}"
                )

                with st.spinner(
                    "🤖 AI Tutor is answering..."
                ):

                    if st.session_state.get(
                        "pdf_loaded",
                        False
                    ):

                        answer = ChatService().ask(
                            st.session_state.vector_db,
                            spoken_text
                        )

                    else:

                        answer = GeminiService().ask(
                            spoken_text
                        )

                st.session_state.chat_history.append(
                    ("You 🎤", spoken_text)
                )

                st.session_state.chat_history.append(
                    ("AI", answer)
                )

                st.success(
                    f"🤖 AI Tutor: {answer}"
                )

            else:

                st.warning(
                    "Could not understand the recording. "
                    "Please try again."
                )

    except Exception as e:

        st.error(
            f"🎤 Voice input unavailable: {e}"
        )

    # --------------------------------------------------
    # CONVERSATION
    # --------------------------------------------------

    st.markdown("---")

    if st.session_state.chat_history:

        st.markdown("### 🗨️ Conversation")

        for speaker, message in st.session_state.chat_history:

            if speaker.startswith("You"):

                with st.chat_message("user"):

                    st.write(message)

            else:

                with st.chat_message("assistant"):

                    st.write(message)
# --------------------------------------------------
# PAGE ROUTER
# --------------------------------------------------

if st.session_state.current_page == "Dashboard":

    st.title("🎓 Educational AI Agent")

    st.subheader(
        "Your Personal AI Learning Assistant"
    )

    st.write(
        "Upload your study material and use AI-powered "
        "tools to learn smarter."
    )

    st.divider()

    st.info(
        "📚 Choose a feature from the sidebar to get started."
    )

# --------------------------------------------------
# PDF UPLOADER
# --------------------------------------------------
if st.session_state.current_page == "Dashboard":

    st.subheader("📚 Study Material")

    uploaded_file = st.file_uploader(
        "📂 Upload your study PDF",
        type=["pdf"],
        key="main_pdf_uploader"
    )

    if uploaded_file is not None:

        is_new_file = (
            st.session_state.get("uploaded_filename", "")
            != uploaded_file.name
        )

        if is_new_file:

            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.pdf_text = ""
            st.session_state.pdf_loaded = False
            st.session_state.vector_db = None

            reader = PDFReader()

            with st.spinner("📖 Reading your PDF..."):

                extracted_text = reader.extract_text(
                    uploaded_file
                )

            if not extracted_text or not extracted_text.strip():

                st.error(
                    "❌ Unable to extract text from this PDF."
                )

            else:

                st.session_state.pdf_text = extracted_text

                try:

                    with st.spinner(
                        "🔎 Preparing your AI study assistant..."
                    ):

                        rag = RAGService()

                        st.session_state.vector_db = (
                            rag.load_pdf(
                                extracted_text
                            )
                        )

                    st.session_state.pdf_loaded = True

                    st.success(
                        "✅ PDF uploaded and ready!"
                    )

                except Exception as e:

                    st.session_state.vector_db = None
                    st.session_state.pdf_loaded = False

                    st.error(
                        f"❌ Unable to create PDF embeddings: {e}"
                    )

        if st.session_state.pdf_text:

            st.success(
                f"📄 {st.session_state.uploaded_filename}"
            )

            with st.expander(
                "👀 View Extracted Text"
            ):

                st.write(
                    st.session_state.pdf_text
                )


# =====================================================
# AI SUMMARY
# =====================================================

if st.session_state.current_page == "AI Summary":

    st.markdown(
        """
        <div class="page-header">
            <div class="page-icon">📚</div>
            <div>
                <div class="page-title">AI Summary</div>
                <div class="page-description">
                    Turn your study material into clear and easy-to-understand notes.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------
    # CHECK PDF
    # -------------------------------------------------

    if not st.session_state.get("pdf_text", "").strip():

        st.markdown(
            """
            <div class="empty-state-card">
                <div class="empty-state-icon">📄</div>
                <div class="empty-state-title">
                    No study material uploaded
                </div>
                <div class="empty-state-text">
                    Upload a PDF from the Dashboard first,
                    then come back here to generate your AI summary.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🏠 Go to Dashboard",
            use_container_width=True,
            key="summary_dashboard_button"
        ):
            st.session_state.current_page = "Dashboard"
            st.rerun()

    else:

        # -------------------------------------------------
        # CURRENT PDF
        # -------------------------------------------------

        st.markdown(
            f"""
            <div class="document-card">
                <div class="document-icon">📄</div>
                <div>
                    <div class="document-label">
                        Current Study Material
                    </div>
                    <div class="document-name">
                        {st.session_state.uploaded_filename}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # -------------------------------------------------
        # GENERATE SUMMARY
        # -------------------------------------------------

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            if st.button(
                "✨ Generate AI Summary",
                use_container_width=True,
                key="generate_summary_button"
            ):

                with st.spinner(
                    "🤖 AI is analyzing your study material..."
                ):

                    try:

                        summary = SummaryGenerator().generate_summary(
                            st.session_state.pdf_text
                        )

                        db.save_history(
                            st.session_state.uploaded_filename,
                            summary,
                            "",
                            ""
                        )

                        st.session_state.summary = summary

                    except Exception as e:

                        st.error(
                            f"❌ Unable to generate summary: {e}"
                        )

        # -------------------------------------------------
        # DISPLAY SUMMARY
        # -------------------------------------------------

        if st.session_state.get("summary", ""):

            st.success("✅ Summary generated successfully!")

            st.markdown(
                """
                <div class="summary-heading">
                    📝 Your AI-Generated Summary
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="summary-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                st.session_state.summary
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # -------------------------------------------------
            # DOWNLOAD PDF
            # -------------------------------------------------

            pdf_path = PDFExporter().export(
                "AI Summary",
                st.session_state.summary,
                "summary.pdf"
            )

            with open(pdf_path, "rb") as file:

                st.download_button(
                    "📥 Download Summary PDF",
                    file,
                    file_name="AI_Summary.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_summary_pdf"
                )
# =====================================================
# AI QUIZ
# =====================================================

if st.session_state.current_page == "AI Quiz":

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    # PAGE HEADER - native Streamlit, no raw HTML
    st.markdown("# ❓ AI Quiz")
    st.caption("Test your knowledge with an AI-generated quiz.")
    st.markdown("---")

    pdf_text = st.session_state.get("pdf_text", "").strip()

    if not pdf_text:
        st.info("📄 No study material uploaded. Upload a PDF from the Dashboard first.")
        if st.button("🏠 Go to Dashboard", use_container_width=True, key="quiz_dashboard_button"):
            st.session_state.current_page = "Dashboard"
            st.rerun()

    else:
        # CURRENT DOCUMENT - native Streamlit, no raw HTML
        filename = st.session_state.get("uploaded_filename", "Study Material")
        st.markdown(f"**📄 Quiz based on:** `{filename}`")
        st.markdown("---")

        # GENERATE QUIZ
        if not st.session_state.quiz_questions:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Generate AI Quiz", use_container_width=True, key="generate_quiz"):
                    with st.spinner("🤖 Creating your personalized quiz..."):
                        try:
                            prompt = f"""
You are an educational quiz generator.

Create a multiple-choice quiz from the following study material.
Generate exactly 5 questions.

For every question provide:
- question
- option A
- option B
- option C
- option D
- correct answer

IMPORTANT:
Do NOT reveal the correct answer in the question itself.

Return ONLY valid JSON in exactly this format:
[
  {{
    "question": "Question",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "answer": "A"
  }}
]

Rules:
1. Generate exactly 5 questions.
2. Questions must be based only on the study material.
3. Each question must have exactly 4 options.
4. The answer must be A, B, C, or D.
5. Return only the JSON array.

Study material:
{pdf_text}
"""
                            response = GeminiService().ask(prompt).strip()
                            import json
                            if response.startswith("```"):
                                response = response.replace("```json", "").replace("```", "").strip()
                            questions = json.loads(response)
                            if not isinstance(questions, list) or len(questions) != 5:
                                raise ValueError("AI did not generate exactly 5 valid questions.")
                            for q in questions:
                                if "question" not in q or "options" not in q or "answer" not in q:
                                    raise ValueError("AI returned an invalid question format.")
                                if any(x not in q["options"] for x in ["A", "B", "C", "D"]):
                                    raise ValueError("A question is missing an option.")
                                if q["answer"] not in ["A", "B", "C", "D"]:
                                    raise ValueError("Invalid correct answer returned by AI.")
                            st.session_state.quiz_questions = questions
                            st.session_state.quiz_answers = {}
                            st.session_state.quiz_submitted = False
                            st.session_state.quiz_score = 0
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Unable to generate quiz: {e}")

        # QUESTIONS
        if st.session_state.quiz_questions:
            st.info("📝 Choose the best answer for each question. Your score will be calculated after submission.")

            for i, q in enumerate(st.session_state.quiz_questions):
                st.markdown(f"### Question {i + 1} of {len(st.session_state.quiz_questions)}")
                st.write(q["question"])
                answer = st.radio(
                    "Select your answer:",
                    ["A", "B", "C", "D"],
                    format_func=lambda x, q=q: f"{x}. {q['options'][x]}",
                    key=f"quiz_answer_{i}",
                    disabled=st.session_state.quiz_submitted
                )
                if not st.session_state.quiz_submitted:
                    st.session_state.quiz_answers[i] = answer
                st.markdown("---")

            # SUBMIT
            if not st.session_state.quiz_submitted:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("✅ Submit Quiz", use_container_width=True, key="submit_quiz"):
                        score = sum(
                            1 for i, q in enumerate(st.session_state.quiz_questions)
                            if st.session_state.quiz_answers.get(i) == q["answer"]
                        )
                        total = len(st.session_state.quiz_questions)
                        st.session_state.quiz_score = score
                        st.session_state.quiz_submitted = True
                        db.save_quiz_score(st.session_state.username, "AI Quiz", score, total)
                        st.rerun()

            # RESULT
            if st.session_state.quiz_submitted:
                total = len(st.session_state.quiz_questions)
                score = st.session_state.quiz_score
                percentage = (score / total) * 100 if total else 0

                st.markdown("## 🏆 Quiz Completed!")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{score}/{total}")
                with col2:
                    st.metric("Percentage", f"{percentage:.1f}%")
                with col3:
                    if percentage >= 80:
                        st.metric("Performance", "Excellent")
                    elif percentage >= 60:
                        st.metric("Performance", "Good")
                    elif percentage >= 40:
                        st.metric("Performance", "Needs Practice")
                    else:
                        st.metric("Performance", "Keep Practicing")

                if percentage >= 80:
                    st.success("🎉 Excellent work! You have a strong understanding of this topic.")
                elif percentage >= 60:
                    st.info("👍 Good job! A little more practice will make you stronger.")
                elif percentage >= 40:
                    st.warning("📚 Keep practicing! Review the study material and try again.")
                else:
                    st.error("💪 Don't give up! Review the material and attempt the quiz again.")

                st.markdown("## 📊 Detailed Results")

                for i, q in enumerate(st.session_state.quiz_questions):
                    user_answer = st.session_state.quiz_answers.get(i)
                    correct_answer = q["answer"]

                    st.markdown(f"### Question {i + 1}")
                    st.write(q["question"])

                    if user_answer == correct_answer:
                        st.success(
                            f"✅ Correct! {user_answer}. {q['options'][user_answer]}"
                        )
                    else:
                        if user_answer:
                            st.error(
                                f"❌ Your answer: {user_answer}. {q['options'][user_answer]}"
                            )
                        else:
                            st.error("❌ You did not answer this question.")
                        st.info(
                            f"✅ Correct answer: {correct_answer}. {q['options'][correct_answer]}"
                        )

                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🔄 Generate New Quiz", use_container_width=True, key="generate_new_quiz"):
                        st.session_state.quiz_questions = []
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = 0
                        st.rerun()


# ============================================================
# FLASHCARDS
# ============================================================

if st.session_state.current_page == "Flashcards":

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []

    if "flashcard_answers" not in st.session_state:
        st.session_state.flashcard_answers = {}

    if "flashcard_submitted" not in st.session_state:
        st.session_state.flashcard_submitted = False

    if "flashcard_score" not in st.session_state:
        st.session_state.flashcard_score = 0

    if "flashcard_results" not in st.session_state:
        st.session_state.flashcard_results = []

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("🧠 Flashcards")

    st.write(
        "Practice important concepts from your study material."
    )

    st.divider()

    # ========================================================
    # GET PDF TEXT
    # ========================================================

    pdf_text = st.session_state.get(
        "pdf_text",
        ""
    ).strip()

    # ========================================================
    # NO PDF UPLOADED
    # ========================================================

    if not pdf_text:

        st.info(
            "📄 No study material uploaded."
        )

        st.write(
            "Upload a PDF from the Dashboard first. "
            "Flashcards will be generated from your study material."
        )

        st.write("")

        if st.button(
            "🏠 Go to Dashboard",
            use_container_width=True,
            key="flashcard_dashboard_button"
        ):

            st.session_state.current_page = "Dashboard"

            st.rerun()

    # ========================================================
    # PDF AVAILABLE
    # ========================================================

    else:

        # ====================================================
        # CURRENT STUDY MATERIAL
        # ====================================================

        filename = st.session_state.get(
            "uploaded_filename",
            "Study Material"
        )

        st.subheader("📄 Study Material")

        st.info(
            f"🧠 Flashcards based on: **{filename}**"
        )

        # ====================================================
        # GENERATE FLASHCARDS
        # ====================================================

        if not st.session_state.flashcards:

            st.divider()

            st.subheader("📝 Flashcard Practice")

            st.write(
                "Generate 5 questions from your study material."
            )

            st.write(
                "Answer each question in your own words "
                "and let AI evaluate your answers."
            )

            st.write("")

            if st.button(
                "🚀 Generate Flashcards",
                use_container_width=True,
                key="generate_flashcards_button"
            ):

                with st.spinner(
                    "🧠 Creating questions from your study material..."
                ):

                    try:

                        # --------------------------------------------
                        # GENERATE QUESTIONS
                        # --------------------------------------------

                        generator = FlashcardGenerator()

                        flashcards = (
                            generator.generate_flashcards(
                                pdf_text
                            )
                        )

                        # --------------------------------------------
                        # VALIDATE RESPONSE
                        # --------------------------------------------

                        if not isinstance(
                            flashcards,
                            list
                        ):

                            raise ValueError(
                                "AI returned an invalid flashcard format."
                            )

                        if len(flashcards) == 0:

                            raise ValueError(
                                "No flashcards were generated."
                            )

                        # Keep maximum 5 questions
                        flashcards = flashcards[:5]

                        # --------------------------------------------
                        # VALIDATE EACH FLASHCARD
                        # --------------------------------------------

                        for card in flashcards:

                            if not isinstance(
                                card,
                                dict
                            ):

                                raise ValueError(
                                    "Invalid flashcard data."
                                )

                            if "question" not in card:

                                raise ValueError(
                                    "Flashcard question is missing."
                                )

                            if "correct_answer" not in card:

                                raise ValueError(
                                    "Flashcard correct answer is missing."
                                )

                        # --------------------------------------------
                        # SAVE FLASHCARDS
                        # --------------------------------------------

                        st.session_state.flashcards = flashcards

                        st.session_state.flashcard_answers = {}

                        st.session_state.flashcard_results = []

                        st.session_state.flashcard_submitted = False

                        st.session_state.flashcard_score = 0

                        st.success(
                            f"✅ {len(flashcards)} questions generated!"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"❌ Unable to generate flashcards: {e}"
                        )

        # ========================================================
        # SHOW QUESTIONS
        # ========================================================

        if st.session_state.flashcards:

            st.divider()

            st.subheader("📝 Answer the Questions")

            st.write(
                "Answer every question in your own words."
            )

            st.write(
                "After answering all questions, click "
                "**Submit All Answers**."
            )

            st.write("")

            # ====================================================
            # QUESTIONS
            # ====================================================

            for i, card in enumerate(
                st.session_state.flashcards
            ):

                st.markdown(
                    f"### 🧠 Question {i + 1} "
                    f"of {len(st.session_state.flashcards)}"
                )

                st.write(
                    card["question"]
                )

                answer = st.text_area(
                    "✍️ Your Answer",
                    key=f"flashcard_answer_{i}",
                    height=120,
                    disabled=(
                        st.session_state.flashcard_submitted
                    ),
                    placeholder="Write your answer here..."
                )

                # --------------------------------------------
                # SAVE ANSWER
                # --------------------------------------------

                if not st.session_state.flashcard_submitted:

                    st.session_state.flashcard_answers[i] = answer

                st.divider()

            # ====================================================
            # SUBMIT ANSWERS
            # ====================================================

            if not st.session_state.flashcard_submitted:

                if st.button(
                    "✅ Submit All Answers",
                    use_container_width=True,
                    key="submit_flashcards_button"
                ):

                    # --------------------------------------------
                    # CHECK EMPTY ANSWERS
                    # --------------------------------------------

                    unanswered = []

                    for i in range(
                        len(st.session_state.flashcards)
                    ):

                        answer = (
                            st.session_state
                            .flashcard_answers
                            .get(i, "")
                            .strip()
                        )

                        if not answer:

                            unanswered.append(
                                i + 1
                            )

                    if unanswered:

                        st.warning(
                            "⚠️ Please answer all questions before submitting."
                        )

                    else:

                        # ----------------------------------------
                        # IMPORT JSON
                        # ----------------------------------------

                        import json

                        score = 0

                        results = []

                        # ----------------------------------------
                        # AI EVALUATION
                        # ----------------------------------------

                        with st.spinner(
                            "🤖 AI is evaluating your answers..."
                        ):

                            try:

                                for i, card in enumerate(
                                    st.session_state.flashcards
                                ):

                                    student_answer = (
                                        st.session_state
                                        .flashcard_answers
                                        .get(
                                            i,
                                            ""
                                        )
                                    )

                                    correct_answer = (
                                        card["correct_answer"]
                                    )

                                    # --------------------------------
                                    # EVALUATION PROMPT
                                    # --------------------------------

                                    evaluation_prompt = f"""
You are an educational answer evaluator.

Evaluate the student's answer against the correct answer.

Question:
{card["question"]}

Student's answer:
{student_answer}

Correct answer:
{correct_answer}

Return ONLY valid JSON.

Use exactly this format:

{{
    "correct": true,
    "score": 1,
    "explanation": "Explain clearly why the student's answer is correct or incorrect.",
    "correct_answer": "Give the correct answer."
}}

Rules:

- "correct" must be true or false.
- "score" must be 1 if the student's answer is substantially correct.
- "score" must be 0 if the student's answer is incorrect.
- Give credit when the student demonstrates the essential concept.
- Ignore minor wording differences.
- Keep the explanation simple and student-friendly.
- Do not add Markdown.
- Return ONLY JSON.
"""

                                    # --------------------------------
                                    # ASK GEMINI
                                    # --------------------------------

                                    response = (
                                        GeminiService()
                                        .ask(
                                            evaluation_prompt
                                        )
                                    )

                                    response = (
                                        response
                                        .strip()
                                    )

                                    # --------------------------------
                                    # REMOVE CODE FENCES
                                    # --------------------------------

                                    if response.startswith(
                                        "```"
                                    ):

                                        response = (
                                            response
                                            .replace(
                                                "```json",
                                                ""
                                            )
                                            .replace(
                                                "```",
                                                ""
                                            )
                                            .strip()
                                        )

                                    # --------------------------------
                                    # PARSE JSON
                                    # --------------------------------

                                    evaluation = json.loads(
                                        response
                                    )

                                    # --------------------------------
                                    # NORMALIZE SCORE
                                    # --------------------------------

                                    evaluation_score = int(
                                        evaluation.get(
                                            "score",
                                            0
                                        )
                                    )

                                    if evaluation_score > 0:

                                        evaluation_score = 1

                                    else:

                                        evaluation_score = 0

                                    evaluation["score"] = (
                                        evaluation_score
                                    )

                                    # --------------------------------
                                    # STORE RESULT
                                    # --------------------------------

                                    results.append(
                                        evaluation
                                    )

                                    score += (
                                        evaluation_score
                                    )

                                # ------------------------------------
                                # TOTAL QUESTIONS
                                # ------------------------------------

                                total = len(
                                    st.session_state.flashcards
                                )

                                # ------------------------------------
                                # SAVE RESULTS
                                # ------------------------------------

                                st.session_state.flashcard_results = (
                                    results
                                )

                                st.session_state.flashcard_score = (
                                    score
                                )

                                st.session_state.flashcard_submitted = (
                                    True
                                )

                                # ------------------------------------
                                # SAVE SCORE TO DATABASE
                                # ------------------------------------

                                try:

                                    if (
                                        "db" in globals()
                                        and st.session_state.get(
                                            "username"
                                        )
                                    ):

                                        db.save_quiz_score(
                                            st.session_state.username,
                                            "Flashcards",
                                            score,
                                            total
                                        )

                                except Exception:

                                    pass

                                # ------------------------------------
                                # REFRESH PAGE
                                # ------------------------------------

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    f"❌ Unable to evaluate answers: {e}"
                                )

            # ========================================================
            # RESULTS
            # ========================================================

            if st.session_state.flashcard_submitted:

                st.divider()

                total = len(
                    st.session_state.flashcards
                )

                score = (
                    st.session_state.flashcard_score
                )

                # --------------------------------------------
                # CALCULATE PERCENTAGE
                # --------------------------------------------

                percentage = (
                    (score / total) * 100
                    if total > 0
                    else 0
                )

                # ====================================================
                # RESULT HEADER
                # ====================================================

                st.subheader(
                    "🎉 Flashcards Completed!"
                )

                # ====================================================
                # SCORE METRICS
                # ====================================================

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "🏆 Score",
                        f"{score}/{total}"
                    )

                with col2:

                    st.metric(
                        "📊 Percentage",
                        f"{percentage:.1f}%"
                    )

                with col3:

                    st.metric(
                        "📝 Questions",
                        total
                    )

                st.write("")

                # ====================================================
                # PERFORMANCE MESSAGE
                # ====================================================

                if percentage >= 80:

                    st.success(
                        "🎉 Excellent! You have a strong understanding "
                        "of the concepts."
                    )

                elif percentage >= 60:

                    st.info(
                        "👍 Good effort! Keep practicing to improve "
                        "your understanding."
                    )

                elif percentage >= 40:

                    st.warning(
                        "📚 You're making progress. Review the material "
                        "and try again."
                    )

                else:

                    st.error(
                        "💪 Keep studying! Review the concepts and "
                        "practice again."
                    )

                # ====================================================
                # DETAILED EVALUATION
                # ====================================================

                st.divider()

                st.subheader(
                    "📊 Detailed Evaluation"
                )

                for i, (card, result) in enumerate(
                    zip(
                        st.session_state.flashcards,
                        st.session_state.flashcard_results
                    )
                ):

                    # --------------------------------------------
                    # QUESTION
                    # --------------------------------------------

                    st.markdown(
                        f"### Question {i + 1}"
                    )

                    st.write(
                        card["question"]
                    )

                    # --------------------------------------------
                    # STUDENT ANSWER
                    # --------------------------------------------

                    st.markdown(
                        "#### ✍️ Your Answer"
                    )

                    student_answer = (
                        st.session_state
                        .flashcard_answers
                        .get(
                            i,
                            ""
                        )
                    )

                    st.info(
                        student_answer
                    )

                    # --------------------------------------------
                    # CORRECT / INCORRECT
                    # --------------------------------------------

                    if result.get(
                        "correct",
                        False
                    ):

                        st.success(
                            "✅ Correct"
                        )

                    else:

                        st.error(
                            "❌ Incorrect"
                        )

                    # --------------------------------------------
                    # EXPLANATION
                    # --------------------------------------------

                    st.markdown(
                        "#### 💡 Explanation"
                    )

                    st.write(
                        result.get(
                            "explanation",
                            "No explanation provided."
                        )
                    )

                    # --------------------------------------------
                    # CORRECT ANSWER
                    # --------------------------------------------

                    st.markdown(
                        "#### 🎯 Correct Answer"
                    )

                    correct_answer_display = (
                        result.get(
                            "correct_answer",
                            card.get(
                                "correct_answer",
                                ""
                            )
                        )
                    )

                    st.success(
                        correct_answer_display
                    )

                    st.divider()

                # ====================================================
                # GENERATE NEW FLASHCARDS
                # ====================================================

                if st.button(
                    "🔄 Generate New Flashcards",
                    use_container_width=True,
                    key="new_flashcards_button"
                ):

                    st.session_state.flashcards = []

                    st.session_state.flashcard_answers = {}

                    st.session_state.flashcard_results = []

                    st.session_state.flashcard_submitted = False

                    st.session_state.flashcard_score = 0

                    st.rerun()
# ============================================================
# AI EVALUATION
# ============================================================

if st.session_state.current_page == "Evaluation":

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("📝 AI Evaluation")

    st.write(
        "Review your quiz performance and understand "
        "which answers you got right or wrong."
    )

    st.divider()

    # ========================================================
    # GET QUIZ DATA
    # ========================================================

    questions = st.session_state.quiz_questions

    answers = st.session_state.quiz_answers

    # ========================================================
    # NO QUIZ AVAILABLE
    # ========================================================

    if not questions:

        st.info(
            "ℹ️ No quiz is available for evaluation."
        )

        st.write(
            "Please go to **❓ AI Quiz**, generate a quiz, "
            "answer all the questions, and submit it first."
        )

        st.write("")

        if st.button(
            "❓ Go to AI Quiz",
            use_container_width=True,
            key="evaluation_go_to_quiz"
        ):

            st.session_state.current_page = "AI Quiz"

            st.rerun()

    # ========================================================
    # QUIZ NOT SUBMITTED
    # ========================================================

    elif not st.session_state.quiz_submitted:

        st.warning(
            "⚠️ Your quiz has not been submitted yet."
        )

        st.write(
            "Complete the quiz from the **AI Quiz** section "
            "and click **Submit Quiz** before viewing the evaluation."
        )

        st.write("")

        if st.button(
            "❓ Go to AI Quiz",
            use_container_width=True,
            key="evaluation_return_quiz"
        ):

            st.session_state.current_page = "AI Quiz"

            st.rerun()

    # ========================================================
    # EVALUATION AVAILABLE
    # ========================================================

    else:

        # ====================================================
        # CALCULATE SCORE
        # ====================================================

        score = 0

        total = len(questions)

        for i, question in enumerate(questions):

            user_answer = answers.get(i)

            correct_answer = question.get(
                "answer"
            )

            if user_answer == correct_answer:

                score += 1

        percentage = (
            (score / total) * 100
            if total > 0
            else 0
        )

        # ====================================================
        # OVERALL RESULT
        # ====================================================

        st.subheader(
            "🎉 Evaluation Complete!"
        )

        st.write(
            f"You scored **{score}/{total}** "
            f"with a percentage of **{percentage:.1f}%**."
        )

        st.write("")

        # ====================================================
        # PERFORMANCE METRICS
        # ====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📝 Total Questions",
                total
            )

        with col2:

            st.metric(
                "✅ Correct Answers",
                score
            )

        with col3:

            st.metric(
                "📊 Score",
                f"{percentage:.1f}%"
            )

        st.divider()

        # ====================================================
        # PERFORMANCE ANALYSIS
        # ====================================================

        st.subheader(
            "🎯 Performance Analysis"
        )

        if percentage >= 80:

            st.success(
                "🏆 Excellent performance! "
                "You have a strong understanding of the topic."
            )

        elif percentage >= 60:

            st.info(
                "👍 Good performance! "
                "You understand many of the concepts. "
                "Review a few areas and practice again."
            )

        elif percentage >= 40:

            st.warning(
                "📚 You're making progress! "
                "Review the study material and practice "
                "the concepts you found difficult."
            )

        else:

            st.error(
                "💪 Keep practicing! "
                "Review the study material carefully "
                "and try the quiz again."
            )

        st.divider()

        # ====================================================
        # DETAILED EVALUATION
        # ====================================================

        st.subheader(
            "📋 Detailed Evaluation"
        )

        for i, question in enumerate(questions):

            user_answer = answers.get(i)

            correct_answer = question.get(
                "answer"
            )

            options = question.get(
                "options",
                {}
            )

            question_text = question.get(
                "question",
                ""
            )

            # ------------------------------------------------
            # QUESTION
            # ------------------------------------------------

            st.markdown(
                f"### Question {i + 1}"
            )

            st.write(
                question_text
            )

            # ------------------------------------------------
            # USER ANSWER
            # ------------------------------------------------

            if user_answer in options:

                st.markdown(
                    "#### ✍️ Your Answer"
                )

                st.write(
                    f"**{user_answer}. "
                    f"{options[user_answer]}**"
                )

            else:

                st.markdown(
                    "#### ✍️ Your Answer"
                )

                st.warning(
                    "You did not answer this question."
                )

            # ------------------------------------------------
            # CORRECT ANSWER
            # ------------------------------------------------

            st.markdown(
                "#### 🎯 Correct Answer"
            )

            if correct_answer in options:

                st.success(
                    f"✅ **{correct_answer}. "
                    f"{options[correct_answer]}**"
                )

            else:

                st.success(
                    f"✅ **{correct_answer}**"
                )

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            if user_answer == correct_answer:

                st.success(
                    "🎉 Your answer is correct!"
                )

            else:

                st.error(
                    "❌ Your answer is incorrect."
                )

                st.info(
                    "💡 Review this concept in your study material "
                    "and try the question again."
                )

            st.divider()

        # ====================================================
        # RETAKE QUIZ
        # ====================================================

        st.subheader(
            "🔄 Want to try again?"
        )

        st.write(
            "Retake the quiz to test your knowledge again."
        )

        if st.button(
            "🔄 Retake Quiz",
            use_container_width=True,
            key="retake_quiz_button"
        ):

            st.session_state.quiz_answers = {}

            st.session_state.quiz_submitted = False

            st.session_state.current_page = "AI Quiz"

            st.rerun()
# ============================================================
# STUDY HISTORY
# ============================================================

if st.session_state.current_page == "AI History":

    st.title("📜 Study History")

    st.write(
        "View your previous study activity and generated content."
    )

    st.divider()

    history = db.get_history()

    # ========================================================
    # NO HISTORY
    # ========================================================

    if len(history) == 0:

        st.info(
            "📭 No study history available yet."
        )

        st.write(
            "Your summaries, quizzes, and flashcards "
            "will appear here as you use the application."
        )

    # ========================================================
    # HISTORY AVAILABLE
    # ========================================================

    else:

        st.subheader(
            "📚 Previous Study Sessions"
        )

        for row in history:

            # -----------------------------------------------
            # HISTORY ITEM
            # -----------------------------------------------

            with st.expander(
                f"📄 {row[1]} | {row[5]}"
            ):

                # -------------------------------------------
                # SUMMARY
                # -------------------------------------------

                if row[2]:

                    st.markdown(
                        "### 📚 Summary"
                    )

                    st.write(
                        row[2]
                    )

                # -------------------------------------------
                # QUIZ
                # -------------------------------------------

                if row[3]:

                    st.markdown(
                        "### ❓ Quiz"
                    )

                    st.write(
                        row[3]
                    )

                # -------------------------------------------
                # FLASHCARDS
                # -------------------------------------------

                if row[4]:

                    st.markdown(
                        "### 🧠 Flashcards"
                    )

                    st.write(
                        row[4]
                    )
# =====================================================
# DASHBOARD - EDUAI
# =====================================================

if st.session_state.current_page == "Dashboard":

    username = st.session_state.username

    # -------------------------------------------------
    # DASHBOARD HEADER
    # -------------------------------------------------

    st.markdown(
        f"""
        <div class="dashboard-header">
            <div>
                <div class="dashboard-title">
                    📚 Learning Dashboard
                </div>
                <div class="dashboard-welcome">
                    👋 Welcome back, <strong>{username}</strong>!
                </div>
                <div class="dashboard-description">
                    Track your learning activity and performance.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='dashboard-space'></div>",
                unsafe_allow_html=True)

    # -------------------------------------------------
    # GET DATA
    # -------------------------------------------------

    study_plans = db.get_study_plans(username)

    quiz_scores = db.get_quiz_scores(username)

    # -------------------------------------------------
    # QUIZ STATISTICS
    # -------------------------------------------------

    percentages = []

    for row in quiz_scores:

        score_value = row[3]
        total_value = row[4]

        if total_value > 0:

            percentage = (
                score_value / total_value
            ) * 100

            percentages.append(percentage)

    if percentages:

        average_score = (
            sum(percentages) /
            len(percentages)
        )

        best_score = max(percentages)

    else:

        average_score = 0
        best_score = 0

    # -------------------------------------------------
    # STATISTICS
    # -------------------------------------------------

    st.markdown(
        "<div class='section-title'>📊 Your Learning Overview</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📅 Study Plans",
            len(study_plans)
        )

    with col2:
        st.metric(
            "📝 Quizzes",
            len(quiz_scores)
        )

    with col3:
        st.metric(
            "📈 Average Score",
            f"{average_score:.1f}%"
        )

    with col4:
        st.metric(
            "🏆 Best Score",
            f"{best_score:.1f}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------
    # AI LEARNING TOOLS
    # -------------------------------------------------

    st.markdown(
        "<div class='section-title'>⚡ AI Learning Tools</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">AI Summary</div>
                <div class="feature-description">
                    Turn your study material into
                    simple, easy-to-understand notes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open AI Summary →",
            use_container_width=True,
            key="dashboard_summary"
        ):
            st.session_state.current_page = "AI Summary"
            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">❓</div>
                <div class="feature-title">AI Quiz</div>
                <div class="feature-description">
                    Test your knowledge with
                    AI-generated questions.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Take AI Quiz →",
            use_container_width=True,
            key="dashboard_quiz"
        ):
            st.session_state.current_page = "AI Quiz"
            st.rerun()

    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Flashcards</div>
                <div class="feature-description">
                    Practice important concepts
                    with interactive questions.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Practice Flashcards →",
            use_container_width=True,
            key="dashboard_flashcards"
        ):
            st.session_state.current_page = "Flashcards"
            st.rerun()

    # -------------------------------------------------
    # SECOND ROW
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Evaluation</div>
                <div class="feature-description">
                    Review your quiz performance
                    and identify areas to improve.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "View Evaluation →",
            use_container_width=True,
            key="dashboard_evaluation"
        ):
            st.session_state.current_page = "Evaluation"
            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">AI Tutor</div>
                <div class="feature-description">
                    Ask questions and learn with
                    your personal AI tutor.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Ask AI Tutor →",
            use_container_width=True,
            key="dashboard_tutor"
        ):
            st.session_state.current_page = "AI Tutor"
            st.rerun()

    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📅</div>
                <div class="feature-title">Study Planner</div>
                <div class="feature-description">
                    Organize your study schedule
                    and stay consistent.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Study Planner →",
            use_container_width=True,
            key="dashboard_planner"
        ):
            st.session_state.current_page = "Study Planner"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
# -------------------------------------------------
# PROGRESS
# -------------------------------------------------

st.subheader("🎯 Learning Progress")

# -------------------------------------------------
# INITIALIZE DATA
# -------------------------------------------------

percentages = []

study_plans = []

# -------------------------------------------------
# GET QUIZ SCORES
# -------------------------------------------------

try:

    username = st.session_state.get(
        "username",
        ""
    )

    quiz_scores = db.get_quiz_scores(
        username
    )

    for row in quiz_scores:

        try:

            score = float(row[2])

            total = float(row[3])

            if total > 0:

                percentage = (
                    score / total
                ) * 100

                percentages.append(
                    percentage
                )

        except (
            ValueError,
            TypeError,
            IndexError
        ):

            continue

except Exception:

    percentages = []


# -------------------------------------------------
# GET STUDY PLANS
# -------------------------------------------------

try:

    username = st.session_state.get(
        "username",
        ""
    )

    study_plans = db.get_study_plans(
        username
    )

except Exception:

    study_plans = []


# -------------------------------------------------
# CALCULATE AVERAGE SCORE
# -------------------------------------------------

if percentages:

    average_score = (
        sum(percentages)
        / len(percentages)
    )

else:

    average_score = 0


# -------------------------------------------------
# OVERALL PROGRESS
# -------------------------------------------------

progress_value = min(
    max(
        average_score / 100,
        0.0
    ),
    1.0
)

st.progress(
    progress_value
)

if percentages:

    st.write(
        f"Your current average performance is "
        f"**{average_score:.1f}%**."
    )

else:

    st.write(
        "Complete your first quiz to start "
        "tracking your learning progress."
    )


# -------------------------------------------------
# PERFORMANCE OVERVIEW
# -------------------------------------------------

st.divider()

st.subheader(
    "📈 Performance Overview"
)

if not percentages:

    st.info(
        "Take a quiz to start tracking your performance."
    )

else:

    fig = go.Figure()

    fig.add_bar(
        x=[
            f"Quiz {i + 1}"
            for i in range(
                len(percentages)
            )
        ],
        y=percentages
    )

    fig.update_layout(
        xaxis_title="Quiz",
        yaxis_title="Score (%)",
        yaxis=dict(
            range=[0, 100]
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -------------------------------------------------
# LEARNING INSIGHT
# -------------------------------------------------

st.divider()

st.subheader(
    "💡 Learning Insight"
)

if not percentages:

    st.info(
        "Complete your first quiz to receive "
        "a learning insight."
    )

elif average_score >= 80:

    st.success(
        "🌟 Excellent performance! "
        "Keep maintaining your study routine."
    )

elif average_score >= 60:

    st.warning(
        "👍 Good progress! "
        "Review weaker topics and practice more."
    )

else:

    st.error(
        "📚 Keep practicing! "
        "Spend more time reviewing your study materials."
    )


# -------------------------------------------------
# RECENT STUDY PLANS
# -------------------------------------------------

st.divider()

st.subheader(
    "📅 Recent Study Plans"
)

if not study_plans:

    st.info(
        "No study plans created yet."
    )

else:

    for plan_data in study_plans[:5]:

        try:

            subjects_saved = plan_data[2]

            exam_date_saved = plan_data[3]

            hours_saved = plan_data[4]

            created_at = plan_data[6]

        except (
            IndexError,
            TypeError
        ):

            continue

        with st.expander(
            f"📅 {exam_date_saved} | {created_at}"
        ):

            st.write(
                f"📚 **Subjects:** {subjects_saved}"
            )

            st.write(
                f"⏰ **Study Time:** "
                f"{hours_saved} hours/day"
            )
# =====================================================
# CHAT WITH PDF + VOICE INPUT - WEEK 4 DAY 4
# =====================================================
if st.session_state.current_page == "AI Chat":

    st.subheader(" AI Chat")
    st.write(
        "Ask questions about your uploaded PDF or chat with AI without a PDF."
    )

    if "vector_db" not in st.session_state:
        st.session_state.vector_db = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "voice_question" not in st.session_state:
        st.session_state.voice_question = ""

    question = st.text_input(
        "Ask your question",
        key="pdf_chat_question"
    )

    if st.button("Ask AI", key="ask_pdf_ai"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("🤖 Thinking..."):

                try:

                    if st.session_state.vector_db is not None:

                        answer = ChatService().ask(
                            st.session_state.vector_db,
                            question
                        )

                    else:

                        answer = GeminiService().ask(
                            question
                        )

                    st.session_state.chat_history.append(
                        ("You", question)
                    )

                    st.session_state.chat_history.append(
                        ("AI", answer)
                    )

                except Exception as e:

                    st.error(
                        f"❌ Unable to answer your question: {e}"
                    )

    st.markdown("---")

    if not st.session_state.chat_history:

        st.info(
            "💬 Ask anything. Upload a PDF if you want answers based on your document."
        )

    else:

        st.subheader("💬 Conversation")

        for speaker, message in st.session_state.chat_history:

            if speaker == "You":

                with st.chat_message("user"):
                    st.write(message)

            else:

                with st.chat_message("assistant"):
                    st.write(message)

    st.markdown("---")

    st.subheader("🎤 Voice Input")

    st.write(
        "Use the microphone below to ask your question."
    )

    voice_service = VoiceService()

    voice_context = voice_service.start_recording()

    if st.button("📝 Convert Voice to Text"):

        spoken_text = voice_service.convert_to_text(
            voice_context
        )

        if spoken_text:

            st.session_state.voice_question = spoken_text

            st.success(
                f"🎤 You said: {spoken_text}"
            )

        else:

            st.warning(
                "Could not understand the recording. Please try again."
            )

    if st.session_state.voice_question:

        st.info(
            f"🎤 Voice Question: {st.session_state.voice_question}"
        )

        if st.button("🤖 Ask Voice Question"):

            voice_question = st.session_state.voice_question

            with st.spinner("🤖 Thinking..."):

                try:

                    if st.session_state.vector_db is not None:

                        answer = ChatService().ask(
                            st.session_state.vector_db,
                            voice_question
                        )

                    else:

                        answer = GeminiService().ask(
                            voice_question
                        )

                    st.session_state.chat_history.append(
                        ("You", voice_question)
                    )

                    st.session_state.chat_history.append(
                        ("AI", answer)
                    )

                    st.session_state.voice_question = ""

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Unable to answer voice question: {e}"
                    )

    # -------------------------------------------------
    # ASK AI
    # -------------------------------------------------
if st.button("🤖 Ask AI"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("🤖 Thinking..."):

            try:

                vector_db = st.session_state.get(
                    "vector_db"
                )

                if vector_db is not None:

                    rag = RAGService()

                    context = rag.search(
                        vector_db,
                        question
                    )

                    if context.strip():

                        gemini = GeminiService()

                        answer = gemini.ask_from_context(
                            context,
                            question
                        )

                    else:

                        answer = (
                            "I couldn't find this information "
                            "in the uploaded PDF."
                        )

                else:

                    gemini = GeminiService()

                    answer = gemini.ask(
                        question
                    )

                st.session_state.chat_history.append(
                    ("You", question)
                )

                st.session_state.chat_history.append(
                    ("AI", answer)
                )

            except Exception as e:

                st.error(
                    f"❌ AI error: {e}"
                )
    # -------------------------------------------------
    # CHAT HISTORY
    # -------------------------------------------------

    st.markdown("---")

    st.subheader("💬 Conversation")

    if len(st.session_state.chat_history) == 0:

        st.info(
            "Ask a question about the uploaded PDF."
        )

    else:

        for speaker, message in st.session_state.chat_history:

            if speaker == "You":

                with st.chat_message("user"):

                    st.write(message)

            else:

                with st.chat_message("assistant"):

                    st.write(message)
# -------------------------------------------------
# AI VOICE OUTPUT
# -------------------------------------------------

if (
    "audio_path" in st.session_state
    and st.session_state.audio_path
):

    st.markdown("---")

    st.subheader("🔊 Listen to AI Answer")

    with open(
        st.session_state.audio_path,
        "rb"
    ) as audio_file:

        audio_bytes = audio_file.read()

    st.audio(
        audio_bytes,
        format="audio/mp3"
    )
# =====================================================
# STUDY PLANNER - WEEK 4 DAY 1
# =====================================================

if st.session_state.current_page == "Study Planner":

    st.subheader("📅 AI Study Planner")

    st.write(
        "Create a personalized study schedule using Gemini AI."
    )

    subjects = st.text_area(
        "📚 Enter your subjects/topics",
        placeholder="""Example:
Operating Systems
DBMS
Machine Learning
Data Structures"""
    )

    exam_date = st.date_input(
        "📅 Select your exam date"
    )

    study_hours = st.number_input(
        "⏰ Available study hours per day",
        min_value=1,
        max_value=12,
        value=3,
        step=1
    )

    if st.button("🚀 Generate Study Plan"):

        if not subjects.strip():

            st.warning(
                "Please enter at least one subject."
            )

        else:

            with st.spinner(
                "🤖 Creating your personalized study plan..."
            ):

                planner = StudyPlanner()

                plan = planner.generate_plan(
                    subjects,
                    exam_date,
                    study_hours
                )

                db.save_study_plan(
                    st.session_state.username,
                    subjects,
                    exam_date,
                    study_hours,
                    plan
                )

            st.success(
                "✅ Study Plan Generated!"
            )

            st.markdown(plan)
st.divider()

st.subheader("📜 Previous Study Plans")

study_plans = db.get_study_plans(
    st.session_state.username
)

if not study_plans:

    st.info("No previous study plans found.")

else:

    for plan_data in study_plans:

        plan_id = plan_data[0]
        username = plan_data[1]
        subjects_saved = plan_data[2]
        exam_date_saved = plan_data[3]
        hours_saved = plan_data[4]
        saved_plan = plan_data[5]
        created_at = plan_data[6]

        with st.expander(
            f"📅 Exam: {exam_date_saved} | Created: {created_at}"
        ):

            st.write(
                f"📚 **Subjects:** {subjects_saved}"
            )

            st.write(
                f"⏰ **Study Hours:** {hours_saved} hours/day"
            )

            st.markdown("---")

            st.markdown(saved_plan)
# =====================================================
# PROGRESS TRACKER - WEEK 4 DAY 3
# =====================================================

if st.session_state.current_page == "Progress":

    st.subheader("📈 Study Progress")

    st.write(
        "Track your quiz performance and learning progress."
    )

    # -------------------------------------------------
    # QUIZ SCORE INPUT
    # -------------------------------------------------

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Operating Systems"
    )

    score = st.number_input(
        "✅ Correct Answers",
        min_value=0,
        value=0,
        step=1
    )

    total = st.number_input(
        "📝 Total Questions",
        min_value=1,
        value=10,
        step=1
    )

    # -------------------------------------------------
    # SAVE SCORE
    # -------------------------------------------------

    if st.button("💾 Save Quiz Score"):

        if not subject.strip():

            st.warning(
                "Please enter a subject."
            )

        elif score > total:

            st.error(
                "Correct answers cannot be greater than total questions."
            )

        else:

            db.save_quiz_score(
                st.session_state.username,
                subject,
                score,
                total
            )

            percentage = (score / total) * 100

            st.success(
                f"✅ Score saved! You scored {percentage:.1f}%."
            )

    # -------------------------------------------------
    # PERFORMANCE
    # -------------------------------------------------

    st.divider()

    st.subheader("📊 Your Performance")

    scores = db.get_quiz_scores(
        st.session_state.username
    )

    if not scores:

        st.info(
            "No quiz scores recorded yet."
        )

    else:

        percentages = []

        for row in scores:

            score_value = row[3]
            total_value = row[4]

            percentage = (
                score_value / total_value
            ) * 100

            percentages.append(
                percentage
            )

        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        average_score = (
            sum(percentages) / len(percentages)
        )

        best_score = max(percentages)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📝 Quizzes Attempted",
                len(scores)
            )

        with col2:

            st.metric(
                "📊 Average Score",
                f"{average_score:.1f}%"
            )

        with col3:

            st.metric(
                "🏆 Best Score",
                f"{best_score:.1f}%"
            )

        # -------------------------------------------------
        # PERFORMANCE CHART
        # -------------------------------------------------

        st.subheader("📈 Quiz Performance")

        fig = go.Figure()

        fig.add_bar(
            x=[
                f"Quiz {i + 1}"
                for i in range(len(percentages))
            ],
            y=percentages
        )

        fig.update_layout(
            xaxis_title="Quiz",
            yaxis_title="Score (%)",
            yaxis=dict(
                range=[0, 100]
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="progress_performance_chart"
        )

        # -------------------------------------------------
        # QUIZ HISTORY
        # -------------------------------------------------

        st.subheader("📜 Quiz History")

        for row in scores:

            percentage = (
                row[3] / row[4]
            ) * 100

            st.write(
                f"📚 **{row[2]}** — "
                f"{row[3]}/{row[4]} "
                f"({percentage:.1f}%)"
            )
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
from backend.services.study_planner import StudyPlanner
from backend.services.voice_service import VoiceService
from backend.services.tts_service import TTSService
import plotly.graph_objects as go

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
    st.write("📅 Study Planner")
    st.write("📈 Progress")

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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    [
        "📚 Summary",
        "❓ Quiz",
        "🧠 Flashcards",
        "📝 Evaluation",
        "📜 History",
        "📊 Dashboard",
        "💬 Chat",
        "📅 Study Planner",
        "📈 Progress"
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
# DASHBOARD - DAY 6
# =====================================================

with tab6:

    st.subheader("📊 Learning Dashboard")

    username = st.session_state.username

    st.write(
        f"👋 Welcome back, **{username}**!"
    )

    st.write(
        "Track your learning activity and performance."
    )

    st.divider()

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

            percentages.append(
                percentage
            )

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
    # DASHBOARD CARDS
    # -------------------------------------------------

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
            "📊 Average Score",
            f"{average_score:.1f}%"
        )

    with col4:

        st.metric(
            "🏆 Best Score",
            f"{best_score:.1f}%"
        )

    st.divider()

    # -------------------------------------------------
    # PERFORMANCE
    # -------------------------------------------------

    st.subheader("📈 Performance Overview")

    if not percentages:

        st.info(
            "Take a quiz to start tracking your performance."
        )

    else:

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
            use_container_width=True
        )

    # -------------------------------------------------
    # LEARNING INSIGHT
    # -------------------------------------------------

    st.subheader("💡 Learning Insight")

    if not percentages:

        st.info(
            "Complete your first quiz to receive a learning insight."
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

    st.subheader("📅 Recent Study Plans")

    if not study_plans:

        st.info(
            "No study plans created yet."
        )

    else:

        for plan_data in study_plans[:5]:

            subjects_saved = plan_data[2]
            exam_date_saved = plan_data[3]
            hours_saved = plan_data[4]
            created_at = plan_data[6]

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

with tab7:

    st.subheader("💬 Chat with Uploaded PDF")

    st.write(
        "Ask questions about the uploaded PDF using text or voice."
    )

    # -------------------------------------------------
    # TEXT QUESTION
    # -------------------------------------------------

    question = st.text_input(
        "⌨️ Type your question",
        placeholder="Example: What is the main topic of this PDF?"
    )

    # -------------------------------------------------
    # SHOW VOICE QUESTION
    # -------------------------------------------------

    if "voice_question" in st.session_state:

        st.info(
            f"🎤 Voice Question: {st.session_state.voice_question}"
        )

        question = st.session_state.voice_question

    # -------------------------------------------------
    # VOICE INPUT
    # -------------------------------------------------

    st.markdown("### 🎤 Voice Input")

    st.write(
        "Use the microphone below to ask your question."
    )

    voice_service = VoiceService()

    voice_context = voice_service.start_recording()

    # -------------------------------------------------
    # CONVERT VOICE TO TEXT
    # -------------------------------------------------

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

    # -------------------------------------------------
    # ASK AI
    # -------------------------------------------------

    if st.button("🤖 Ask AI"):

        final_question = question.strip()

        if not final_question:

            st.warning(
                "Please type or speak a question."
            )

        elif "vector_db" not in st.session_state:

            st.error(
                "Please upload a PDF before asking questions."
            )

        else:

            with st.spinner(
                "🔎 Searching the uploaded PDF..."
            ):

                answer = ChatService().ask(
                    st.session_state.vector_db,
                    final_question
                )

                # Generate voice for AI answer
                tts = TTSService()

                audio_path = tts.generate_audio(
                    answer
                )

                st.session_state.audio_path = audio_path    
                
            st.session_state.chat_history.append(
                ("You", final_question)
            )

            st.session_state.chat_history.append(
                ("AI", answer)
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

with tab8:

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

with tab9:

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
            use_container_width=True
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
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os
import smtplib
from email.mime.text import MIMEText


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="VisionStudy AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       MAIN APPLICATION
       ========================================= */

    .stApp {
        background: #f7f9fc;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =========================================
       HERO SECTION
       ========================================= */

    .hero {
        background: linear-gradient(
            135deg,
            #667eea 0%,
            #764ba2 100%
        );

        padding: 2.2rem 2.5rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 1.8rem;

        box-shadow:
            0 12px 35px rgba(102, 126, 234, 0.22);
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.94;
        line-height: 1.6;
    }


    /* =========================================
       SECTION TITLES
       ========================================= */

    .section-title {
        font-size: 1.4rem;
        font-weight: 750;
        color: #202938;
        margin-top: 1.2rem;
        margin-bottom: 0.9rem;
    }


    /* =========================================
       CARDS
       ========================================= */

    .card {
        background: white;
        border-radius: 18px;
        padding: 1.4rem;

        margin-bottom: 1rem;

        border: 1px solid #e8ecf3;

        box-shadow:
            0 6px 22px rgba(30, 41, 59, 0.06);
    }


    /* =========================================
       EXPLANATION CARD
       ========================================= */

    .explanation-card {
        background: white;

        border-left: 5px solid #667eea;

        border-radius: 16px;

        padding: 1.6rem;

        margin-top: 1rem;
        margin-bottom: 1.2rem;

        box-shadow:
            0 6px 22px rgba(30, 41, 59, 0.06);

        line-height: 1.7;
    }


    /* =========================================
       CHAT
       ========================================= */

    .user-message {
        background: #667eea;
        color: white;

        padding: 1rem 1.2rem;

        border-radius:
            16px 16px 5px 16px;

        margin:
            0.7rem 0 0.7rem 15%;

        line-height: 1.6;
    }

    .ai-message {
        background: white;
        color: #202938;

        padding: 1rem 1.2rem;

        border-radius:
            16px 16px 16px 5px;

        border: 1px solid #e5e9f2;

        margin:
            0.7rem 15% 0.9rem 0;

        box-shadow:
            0 4px 14px rgba(30, 41, 59, 0.05);

        line-height: 1.6;
    }


    /* =========================================
       SIDEBAR
       ========================================= */

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8ecf3;
    }

    .sidebar-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #667eea;
    }

    .sidebar-text {
        color: #667085;
        font-size: 0.9rem;
        line-height: 1.65;
    }


    /* =========================================
       BUTTONS
       ========================================= */

    .stButton > button {
        border-radius: 11px;

        font-weight: 650;

        min-height: 44px;

        border: 1px solid #d8def0;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 5px 14px rgba(30, 41, 59, 0.10);
    }


    /* =========================================
       TEXT INPUTS
       ========================================= */

    .stTextInput input,
    .stTextArea textarea {
        border-radius: 11px !important;
    }


    /* =========================================
       FILE UPLOADER
       ========================================= */

    [data-testid="stFileUploader"] {
        background: white;

        border-radius: 16px;

        padding: 0.6rem;

        border: 1px dashed #cbd5e1;
    }


    /* =========================================
       SUCCESS MESSAGE
       ========================================= */

    .success-box {
        background: #ecfdf3;

        border: 1px solid #abefc6;

        color: #067647;

        padding: 0.8rem 1rem;

        border-radius: 10px;

        margin-top: 0.7rem;
    }


    /* =========================================
       FOOTER
       ========================================= */

    .footer {
        text-align: center;

        color: #98a2b3;

        font-size: 0.85rem;

        margin-top: 2.5rem;

        padding-top: 1.2rem;

        border-top: 1px solid #e5e7eb;
    }


    /* =========================================
       MOBILE RESPONSIVE
       ========================================= */

    @media (max-width: 768px) {

        .hero {
            padding: 1.6rem;
        }

        .hero-title {
            font-size: 1.8rem;
        }

        .hero-subtitle {
            font-size: 0.95rem;
        }

        .user-message {
            margin-left: 5%;
        }

        .ai-message {
            margin-right: 5%;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CHECK GEMINI API KEY
# =========================================================

if not GEMINI_API_KEY:

    st.error(
        "Gemini API key not found. "
        "Please check your .env file."
    )

    st.stop()


# =========================================================
# CONFIGURE GEMINI
# =========================================================

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-3.8-flash"
)


# =========================================================
# SESSION STATE
# =========================================================

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================================================
# EMAIL FUNCTION
# =========================================================

def send_email(to_address, subject, body):

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = GMAIL_ADDRESS
    message["To"] = to_address

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD
        )

        server.send_message(message)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📚 VisionStudy AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="sidebar-text">
        Your AI-powered study assistant that understands
        questions, diagrams, notes and educational images.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ✨ Features")

    st.markdown(
        """
        📷 **Vision Analysis**  
        Understand study images

        💡 **Smart Explanation**  
        Get simple explanations

        💬 **AI Chat**  
        Ask follow-up questions

        📧 **Email**  
        Send explanations by email
        """
    )

    st.divider()

    st.markdown("### 🚀 How to use")

    st.markdown(
        """
        **1.** Upload a study image

        **2.** Ask a question or let AI analyze it

        **3.** Read the explanation

        **4.** Ask follow-up questions

        **5.** Email the explanation
        """
    )

    st.divider()

    st.caption("Powered by Gemini AI")


# =========================================================
# HERO SECTION
# =========================================================

# =========================================================
# HERO SECTION
# =========================================================

st.title("📚 VisionStudy AI")

st.write(
    "Snap it. Understand it. Learn it. "
    "Your intelligent AI vision study assistant."
)

# =========================================================
# IMAGE UPLOAD
# =========================================================

st.markdown(
    '<div class="section-title">📷 Upload Your Study Material</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a question, diagram, notes or study image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]
)

# =========================================================
# IMAGE PROCESSING
# =========================================================
# =========================================================
# IMAGE PROCESSING
# =========================================================

# Default values
image = None
question = ""
analyze_button = False

if uploaded_file:

    try:

        image = Image.open(uploaded_file)

        # Validate image
        image.verify()

        # Re-open image after verification
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(
            [1, 1],
            gap="large"
        )

        # -------------------------------------------------
        # LEFT: IMAGE PREVIEW
        # -------------------------------------------------

        with col1:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.image(
                image,
                caption="Your Study Material",
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # RIGHT: QUESTION
        # -------------------------------------------------

        with col2:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.markdown(
                "### 🔍 What do you want to know?"
            )

            question = st.text_area(
                "Your question",
                placeholder=(
                    "Example:\n"
                    "• Explain this step by step\n"
                    "• What is this concept?\n"
                    "• Solve this problem"
                ),
                height=160,
                label_visibility="collapsed"
            )

            analyze_button = st.button(
                "🔍 Analyze Image",
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    except Exception:

        st.error(
            "❌ This file could not be processed. "
            "Please upload a valid JPG, JPEG, PNG or WEBP image."
        )

        st.stop()
# =====================================================
# ANALYZE IMAGE
# =====================================================

if analyze_button:

    with st.spinner(
        "🤖 Gemini is analyzing your study material..."
    ):

        if question.strip():

            user_prompt = question

        else:

            user_prompt = """
            Analyze this study image carefully.

            Explain the important content in simple English.

            If there is a problem:
            - Identify the problem
            - Explain the method
            - Show the solution step by step

            If there is a diagram:
            - Identify the components
            - Explain their purpose
            - Explain how they work together

            If there are notes:
            - Summarize the important concepts
            - Explain difficult terms simply
            """

        try:

            # -------------------------------------------------
            # STRUCTURED AI PROMPT
            # -------------------------------------------------

            structured_prompt = f"""
You are VisionStudy AI, an intelligent and friendly
AI study assistant.

Analyze the uploaded educational image carefully.

Student's request:
{user_prompt}

Give the response in the following format:

## 📌 Quick Summary

Give a short and easy summary of the main content.

## 🔑 Important Points

Give the most important points the student should remember.

## 📖 Simple Explanation

Explain the topic step by step in simple English.
Assume the student is a beginner.

## ❓ Possible Exam Questions

Give 3 to 5 useful questions that could be asked
from this topic in an exam.

## 💡 Easy Example

Give one simple real-world or practical example
when applicable.

Rules:

- Use simple English.
- Keep the explanation educational and accurate.
- Explain difficult terms in simple words.
- If the image contains a mathematical problem,
  solve it step by step.
- If the image contains a programming problem,
  explain the logic and solution step by step.
- If the image contains a diagram,
  explain its components and how they work together.
- If the image contains notes,
  identify and explain the important concepts.
- If the image contains a timetable or schedule,
  clearly summarize the important information.
- Do not invent information that is not visible
  or reasonably inferable from the image.
- Make the answer easy for a college student to study.
"""

            # -------------------------------------------------
            # GEMINI VISION ANALYSIS
            # -------------------------------------------------

            response = model.generate_content(
                [
                    structured_prompt,
                    image
                ]
            )

            # -------------------------------------------------
            # SAVE EXPLANATION
            # -------------------------------------------------

            st.session_state.explanation = response.text

            # Reset chat for new image
            st.session_state.chat_history = []

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )

# =========================================================
# EXPLANATION SECTION
# =========================================================

if st.session_state.explanation:

    st.markdown(
        '<div class="section-title">💡 AI Explanation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="explanation-card">',
        unsafe_allow_html=True
    )

    st.write(
        st.session_state.explanation
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # EMAIL SECTION
    # =====================================================

    st.markdown(
        '<div class="section-title">📧 Save & Share</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(
            "### 📩 Send Explanation by Email"
        )

        recipient_email = st.text_input(
            "Recipient Email",
            placeholder="example@gmail.com"
        )

        send_email_button = st.button(
            "📨 Send Explanation",
            use_container_width=True
        )

        if send_email_button:

            if not recipient_email:

                st.warning(
                    "Please enter a recipient email address."
                )

            elif (
                not GMAIL_ADDRESS
                or not GMAIL_APP_PASSWORD
            ):

                st.error(
                    "Gmail credentials not found. "
                    "Please check your .env file."
                )

            else:

                try:

                    send_email(
                        recipient_email,
                        "VisionStudy AI - Study Explanation",
                        st.session_state.explanation
                    )

                    st.success(
                        "✅ Explanation sent successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Email sending failed: {e}"
                    )


    # =====================================================
    # CHAT SECTION
    # =====================================================

    st.markdown(
        '<div class="section-title">💬 Study Chat</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Ask anything about the uploaded study material."
    )


    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    follow_up = st.text_input(
        "Ask AI",
        placeholder=(
            "Example: Explain this in very simple words..."
        ),
        label_visibility="collapsed"
    )


    chat_col1, chat_col2 = st.columns(
        [3, 1]
    )


    with chat_col1:

        ask_button = st.button(
            "🤖 Ask AI",
            use_container_width=True
        )


    with chat_col2:

        clear_button = st.button(
            "🗑️ Clear",
            use_container_width=True
        )


    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if clear_button:

        st.session_state.chat_history = []

        st.rerun()


    # =====================================================
    # ASK AI
    # =====================================================

    if ask_button:

        if not follow_up.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            with st.spinner(
                "🤖 AI is thinking..."
            ):

                try:

                    chat_prompt = f"""
You are VisionStudy AI, a friendly AI study assistant.

The student uploaded a study image.

Original AI explanation:
{st.session_state.explanation}

Student's question:
{follow_up}

Answer the student's question clearly.

Rules:
- Use simple English.
- Explain step by step when necessary.
- Assume the student is a beginner.
- Give a simple example when useful.
- Focus on the uploaded study material.
- Do not make the answer unnecessarily complicated.
"""

                    chat_response = model.generate_content(
                        [
                            chat_prompt,
                            image
                        ]
                    )


                    st.session_state.chat_history.append(
                        {
                            "question": follow_up,
                            "answer": chat_response.text
                        }
                    )

                    st.rerun()


                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


    # =====================================================
    # CHAT HISTORY
    # =====================================================

    if st.session_state.chat_history:

        st.markdown(
            "### 📖 Conversation"
        )

        for chat in st.session_state.chat_history:

            # User message
            st.markdown(
                f"""
                <div class="user-message">

                <strong>🧑 You</strong><br><br>

                {chat["question"]}

                </div>
                """,
                unsafe_allow_html=True
            )


            # AI message
            st.markdown(
                f"""
                <div class="ai-message">

                <strong>🤖 VisionStudy AI</strong><br><br>

                {chat["answer"]}

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.markdown(
        """
        <div class="card" style="text-align:center; padding:3rem;">

        <div style="font-size:3rem;">📚</div>

        <h2>Start Learning with AI</h2>

        <p style="color:#667085;">
        Upload a question, diagram, programming problem,
        mathematics problem or study note to get started.
        </p>

        <p style="color:#98A2B3;">
        Supported formats: JPG • JPEG • PNG • WEBP
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        📚 VisionStudy AI &nbsp;•&nbsp; AI-powered Study Assistant
        <br>
        Learn smarter with AI ✨
    </div>
    """,
    unsafe_allow_html=True
)
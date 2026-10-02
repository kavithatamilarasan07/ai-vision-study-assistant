# 📚 VisionStudy AI

### AI-Powered Vision Study Assistant

VisionStudy AI is an AI-powered study assistant that uses computer vision and generative AI to understand educational images and provide simple, structured explanations.

Students can upload questions, diagrams, notes, programming problems, mathematics problems, or study schedules and interact with the AI for better understanding.

---

## ✨ Features

- 📷 Upload educational images
- 🤖 AI-powered image analysis
- 📌 Quick summaries
- 🔑 Important points
- 📖 Simple step-by-step explanations
- ❓ Possible exam questions
- 💡 Easy examples
- 💬 Follow-up AI study chat
- 📧 Send explanations through email
- 🛡️ Image validation and error handling
- 📱 Responsive and user-friendly interface

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Generative AI
- Pillow (PIL)
- Python-dotenv
- SMTP / Gmail
- HTML
- CSS

---

## 🧠 How It Works

```text
Student
   ↓
Upload Study Image
   ↓
VisionStudy AI
   ↓
Gemini Vision Analysis
   ↓
Structured Explanation
   ↓
Follow-up Questions
   ↓
AI Study Chat
   ↓
Email Explanation
📂 Project Structure
ai-vision-study-assistant/
│
├── app.py
├── prompts.py
├── README.md
├── .gitignore
│
└── .env

.env contains private API credentials and should never be uploaded to GitHub.

⚙️ Installation
1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
2. Open the project
cd ai-vision-study-assistant
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment

Windows:

.venv\Scripts\activate
5. Install dependencies
pip install streamlit google-generativeai python-dotenv pillow
🔐 Environment Variables

Create a .env file:

GEMINI_API_KEY=your_gemini_api_key
GMAIL_ADDRESS=your_gmail_address
GMAIL_APP_PASSWORD=your_gmail_app_password

Never share or upload your actual API key or Gmail App Password.

▶️ Run the Application
streamlit run app.py

The application will open in your browser.

📚 Supported Study Materials

VisionStudy AI can be used with:

📖 Study notes
🧮 Mathematics problems
💻 Programming questions
📊 Diagrams
📝 Exam questions
📅 Timetables
🔬 Educational images
🎯 Project Objective

The main objective of VisionStudy AI is to make learning easier by allowing students to upload educational content and receive clear, beginner-friendly explanations using AI vision technology.

🚀 Future Enhancements
Voice-based interaction
Multi-language explanations
PDF document analysis
AI-generated quizzes
Personalized study plans
Text-to-speech explanations
Learning progress tracking
👩‍💻 Developer

Kavitha Tamilarasan

B.Sc. Artificial Intelligence and Machine Learning

📄 License

This project is developed for educational and academic purposes.



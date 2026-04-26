# AI Resume Analyzer

AI Resume Analyzer is a full-stack application that helps candidates bridge the gap between their current skills and their dream job. By analyzing a candidate's resume against a target job description, the system provides a comprehensive skill gap analysis, simulates an AI-driven technical interview to assess proficiency, and generates a highly personalized learning roadmap using Retrieval-Augmented Generation (RAG).

## 🚀 Features

- **Smart Resume Parsing**: Extracts key skills, experience, and education from uploaded resumes (PDF/Docx) and compares them against target job descriptions.
- **Skill Gap Analysis**: Identifies missing skills and areas for improvement.
- **AI Mock Interview Assessment**: Generates dynamic interview questions based on the candidate's skills and evaluates their answers to determine true proficiency.
- **RAG-Powered Learning Plans**: Recommends curated learning resources (courses, documentation, tutorials) tailored to the exact skills the candidate needs to master.

## 🧠 Architecture & Models

### Backend (FastAPI)
- **Framework**: Python 3.x with FastAPI for high-performance async API endpoints.
- **LLM Engine**: Powered by **Groq** (using the `llama-3.1-8b-instant` model) for blazing-fast inference, text extraction, gap analysis, and interview evaluations.
- **Vector Store & RAG**: Uses **FAISS** (Facebook AI Similarity Search) and the **Sentence-Transformers** library (`all-MiniLM-L6-v2` model) to convert learning resources into vector embeddings and retrieve the most relevant tutorials based on identified skill gaps.

### Frontend (React + Vite)
- **Framework**: React.js bootstrapped with Vite for instant server start and lightning-fast HMR.
- **Styling**: Tailwind CSS for a beautiful, responsive, and modern user interface.

---

## 🛠️ Local Setup Instructions

Follow these steps to run the application locally on your machine.

### 1. Clone the repository
```bash
git clone https://github.com/PrinceRaghav865037/Resume.git
cd ResumeAnalyser
```

### 2. Backend Setup
1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
2. **Activate the virtual environment:**
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`
3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Create a `.env` file in the root directory (where `requirements.txt` is) and add your Groq API key:
   ```env
   PROJECT_NAME="AI Resume Analyzer"
   VERSION="1.0.0"
   GROQ_API_KEY="your_groq_api_key_here"
   ```
5. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   *The API will be available at `http://127.0.0.1:8000`. The first time you run this, it may take a few minutes to download the Sentence-Transformers AI model.*

### 3. Frontend Setup
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install Node dependencies:**
   ```bash
   npm install
   ```
3. **Start the development server:**
   ```bash
   npm run dev
   ```
   *The UI will be available at `http://localhost:5173`.*

---

## ☁️ Deployment

- **Backend**: Can be deployed to platforms like Render, Heroku, or AWS. The included `requirements.txt` is fully compatible with Render's Python environment.
- **Frontend**: Can be deployed to Vercel, Netlify, or Render static sites using `npm run build`. 

*Note: If deploying the frontend to production, remember to update the API endpoint URL in `frontend/src/App.jsx` from localhost to your deployed backend URL.*

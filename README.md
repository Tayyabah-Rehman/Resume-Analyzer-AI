# 📄 Resume Analyzer AI

![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58.0-red)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered resume analysis tool that evaluates resumes against job descriptions using Groq's Llama 3.3 API. Built for the SoftGrid Solutions AI/ML Engineering internship assessment.

---

## 📹 Demo Video

[![Download Demo Video](https://img.shields.io/badge/📹%20Download-Watch%20Demo%20Video-blue?style=for-the-badge)](https://github.com/Tayyabah-Rehman/Resume-Analyzer-AI/blob/main/Demo_Resume%20Analyzer.mp4)

**Instructions:** Click the button above to download the video file to your computer, then open it to watch the demo.

**What the demo shows:**
- 📄 Uploading a resume (PDF/DOCX)
- 💼 Pasting a job description
- 🤖 AI analysis in action
- 📊 Viewing scores (Overall, CV Standout, ATS, Job Match)
- 📥 Downloading HTML and PDF reports

**Note:** GitHub cannot preview video files directly. The file will download when you click the link.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Upload** | Support PDF and DOCX files |
| 💼 **Job Description Matching** | Paste any JD for targeted analysis |
| ⭐ **4 Scoring Metrics** | Overall, CV Standout, ATS, Job Match (1-10) |
| ✅ **Strengths Analysis** | Identifies what's working well |
| ⚠️ **Weaknesses Detection** | Spots areas needing improvement |
| ❌ **Missing Sections** | Finds important missing resume sections |
| 💡 **Actionable Suggestions** | Specific improvements to implement |
| 🔑 **Keyword Analysis** | Shows present vs missing keywords |
| 📊 **ATS Compatibility** | How well bots can parse your resume |
| 📥 **Report Export** | Download as HTML or PDF |
| 🎯 **Final Recommendation** | Overall hiring fit assessment |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Frontend** | Streamlit |
| **AI Model** | Groq Llama 3.3 (70B) |
| **PDF Processing** | PyPDF |
| **DOCX Processing** | python-docx |
| **PDF Reports** | fpdf2 |
| **API Calls** | Requests |
| **Environment** | Python 3.10/3.11 |

---

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.10 or 3.11 installed
- Groq API key (free from [console.groq.com](https://console.groq.com))
- Internet connection for API calls

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tayyabah-Rehman/Resume-Analyzer-AI.git
cd Resume-Analyzer-AI
```

### 2. Create virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from [console.groq.com](https://console.groq.com)

### 5. Run the application

```bash
streamlit run app.py
```
or run main file 

Open your browser to `http://localhost:8501`

---

## 📝 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Tayyabah Rehman**
🔗 [github.com/Tayyabah-Rehman](https://github.com/Tayyabah-Rehman)

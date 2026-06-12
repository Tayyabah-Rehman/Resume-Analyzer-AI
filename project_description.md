# Resume Analyzer AI — Project Description

## Project Title
Resume Analyzer AI

## Submitted To
SoftGrid Solutions — Internship Assessment

## Submitted By
Tayyabah Rehman
MPhil Artificial Intelligence, University of the Punjab, Lahore
GitHub: https://github.com/Tayyabah-Rehman

---

## Project Overview

Resume Analyzer AI is an intelligent web application that analyzes resumes (PDF or DOCX) using a Large Language Model (LLM) and provides comprehensive, structured feedback. The application evaluates resumes against multiple criteria including overall quality, ATS (Applicant Tracking System) compatibility, CV standout potential, and — when a job description is provided — job-specific match scoring.

The tool is designed to help job seekers understand the strengths and gaps in their resumes and receive actionable, AI-driven improvement suggestions.

---

## Tech Stack

| Component        | Technology                        |
|------------------|-----------------------------------|
| Frontend / UI    | Streamlit                         |
| Backend / Logic  | Python 3.10                       |
| AI Model         | Groq API — LLaMA 3.3 70B Versatile|
| PDF Parsing      | pypdf                             |
| DOCX Parsing     | python-docx                       |
| PDF Generation   | fpdf2                             |
| Config Mgmt      | python-dotenv                     |
| HTTP Requests    | requests                          |

---

## Features

- Upload resume in PDF or DOCX format
- Paste a job description for targeted job-match scoring
- AI-powered structured analysis with 4 scores:
  - Overall Resume Score (1–10)
  - CV Standout Score (1–10) — how memorable the resume is to a recruiter
  - ATS Compatibility Score (1–10) — how well it passes automated screening
  - Job Match Score (1–10) — only shown when a job description is provided
- Detailed breakdown of:
  - Strengths
  - Weaknesses
  - Missing Sections
  - Improvement Suggestions
  - Keywords Present and Missing
  - Final Recommendation
- Download the full analysis report as:
  - HTML (styled, browser-ready)
  - PDF (clean formatted document)
- Fully interactive web interface

---

## How It Works

1. User uploads their resume (PDF or DOCX)
2. User optionally pastes a job description
3. Text is extracted from the uploaded file using pypdf or python-docx
4. Extracted text + job description are sent to Groq's LLaMA 3.3 model via REST API
5. The model returns a structured JSON analysis
6. The app parses the JSON and renders it in a clean Streamlit UI
7. User can download the report as HTML or PDF

---

## Project Structure

```
Resume_Analyzer_AI/
├── app.py                  # Main application
├── .env                    # API key (not committed to git)
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignores .env, venv, __pycache__
└── venv/                   # Virtual environment (not committed)
```

---

## Setup Instructions

```bash
# 1. Clone or download the project
cd Resume_Analyzer_AI

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key to .env
echo GEMINI_API_KEY=your_groq_api_key_here > .env

# 5. Run the app
streamlit run app.py
```

---

## Job Description Match — Asapp Studio (AI/ML Developer Associate)

This project was tested against the AI/ML Developer (Associate) position at Asapp Studio, Lahore.

**Role Requirements vs. Resume Alignment:**
- Python proficiency — Covered
- TensorFlow, PyTorch, Scikit-learn — Covered
- ML model development — Covered
- Data preprocessing and analysis — Covered
- Bachelor's in CS/Data Science — Covered (MPhil AI in progress — exceeds requirement)
- GitHub portfolio — Available at github.com/Tayyabah-Rehman
- Fresh graduate / max 1 year experience — Matches profile

The Resume Analyzer AI tool itself demonstrates hands-on ability to build and deploy AI-integrated applications — directly relevant to the role.

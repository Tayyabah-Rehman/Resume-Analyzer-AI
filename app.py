import streamlit as st
import pypdf
import docx
import os
import io
import requests
import json
from dotenv import load_dotenv
from fpdf import FPDF, XPos, YPos

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def extract_text_from_pdf(file_bytes):
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])


def analyze_resume(resume_text, job_description=""):
    has_jd = bool(job_description.strip())

    jd_instruction = (
        "The candidate has provided a job description. Rate the resume BOTH for overall quality AND for job match."
        if has_jd else
        "No job description provided. Rate the resume for overall quality and market readiness only."
    )

    jd_fields = '"job_match_score": <number 1-10>, "job_match_verdict": "<one sentence on fit for this role>",' if has_jd else ""
    jd_text = ("Job Description:\n" + job_description) if has_jd else ""

    prompt = (
        "You are an expert resume analyzer, ATS specialist, and career coach.\n\n"
        "Analyze the resume below and return your analysis in the EXACT JSON format specified. No extra text, just valid JSON.\n\n"
        + jd_instruction + "\n\n"
        "Return this exact JSON structure:\n"
        "{\n"
        '  "overall_score": <number 1-10>,\n'
        '  "overall_verdict": "<one sentence summary>",\n'
        + ("  " + jd_fields + "\n" if jd_fields else "") +
        '  "cv_standout_score": <number 1-10>,\n'
        '  "cv_standout_verdict": "<one sentence on how memorable/impressive this CV is>",\n'
        '  "ats_score": <number 1-10>,\n'
        '  "ats_verdict": "<one sentence on ATS compatibility>",\n'
        '  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],\n'
        '  "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],\n'
        '  "missing_sections": ["<section 1>", "<section 2>"],\n'
        '  "improvement_suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>", "<suggestion 4>"],\n'
        '  "keywords_present": ["<keyword 1>", "<keyword 2>", "<keyword 3>"],\n'
        '  "keywords_missing": ["<keyword 1>", "<keyword 2>", "<keyword 3>"],\n'
        '  "final_recommendation": "<2-3 sentence overall advice for this candidate>"\n'
        "}\n\n"
        + (jd_text + "\n\n" if jd_text else "") +
        "Resume:\n" + resume_text
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.3
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        raw = response.json()["choices"][0]["message"]["content"]
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    else:
        raise Exception(f"API Error {response.status_code}: {response.json()}")


def build_html_report(data, has_jd, resume_name):
    strengths_li = "".join("<li>" + s + "</li>" for s in data["strengths"])
    weaknesses_li = "".join("<li>" + w + "</li>" for w in data["weaknesses"])
    missing_li = "".join("<li>" + m + "</li>" for m in data["missing_sections"])
    suggestions_li = "".join("<li>" + i + "</li>" for i in data["improvement_suggestions"])
    kw_present = "".join('<span class="tag tag-green">' + k + "</span>" for k in data["keywords_present"])
    kw_missing = "".join('<span class="tag tag-red">' + k + "</span>" for k in data["keywords_missing"])

    jd_card = ""
    if has_jd:
        jd_score = data.get("job_match_score", 0)
        jd_verdict = data.get("job_match_verdict", "")
        jd_card = (
            '<div class="score-card">'
            '<div class="score-label">Job Match Score</div>'
            '<div class="score-value">' + str(jd_score) + '<span class="score-max">/10</span></div>'
            '<div class="score-bar"><div class="score-fill" style="width:' + str(jd_score * 10) + '%; background:#6366f1;"></div></div>'
            '<div class="score-verdict">' + jd_verdict + "</div>"
            "</div>"
        )

    overall_score = data["overall_score"]
    standout_score = data["cv_standout_score"]
    ats_score = data["ats_score"]

    return (
        "<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n"
        "<title>Resume Analysis - " + resume_name + "</title>\n"
        "<style>\n"
        "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
        "body { font-family: 'Segoe UI', sans-serif; background: #f8fafc; color: #1e293b; padding: 40px 20px; }\n"
        ".container { max-width: 900px; margin: auto; }\n"
        "h1 { font-size: 2rem; color: #0f172a; margin-bottom: 4px; }\n"
        ".subtitle { color: #64748b; margin-bottom: 32px; font-size: 0.95rem; }\n"
        ".scores-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px; }\n"
        ".score-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }\n"
        ".score-label { font-size: 0.8rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }\n"
        ".score-value { font-size: 2.5rem; font-weight: 700; color: #0f172a; line-height: 1; }\n"
        ".score-max { font-size: 1rem; color: #94a3b8; }\n"
        ".score-bar { height: 6px; background: #e2e8f0; border-radius: 99px; margin: 10px 0; overflow: hidden; }\n"
        ".score-fill { height: 100%; border-radius: 99px; background: #22c55e; }\n"
        ".score-verdict { font-size: 0.82rem; color: #64748b; margin-top: 6px; }\n"
        ".section { background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }\n"
        ".section h2 { font-size: 1.1rem; font-weight: 700; margin-bottom: 16px; color: #0f172a; }\n"
        "ul { padding-left: 20px; }\n"
        "ul li { margin-bottom: 8px; font-size: 0.92rem; line-height: 1.5; color: #334155; }\n"
        ".tag { display: inline-block; padding: 4px 10px; border-radius: 99px; font-size: 0.8rem; margin: 3px; font-weight: 500; }\n"
        ".tag-green { background: #dcfce7; color: #166534; }\n"
        ".tag-red { background: #fee2e2; color: #991b1b; }\n"
        ".final { background: #0f172a; color: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; }\n"
        ".final h2 { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; }\n"
        ".final p { font-size: 1rem; line-height: 1.7; color: #e2e8f0; }\n"
        ".footer { text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 32px; }\n"
        "</style>\n</head>\n<body>\n<div class='container'>\n"
        "<h1>Resume Analysis Report</h1>\n"
        "<div class='subtitle'>File: " + resume_name + " | Generated by Resume Analyzer AI</div>\n"
        "<div class='scores-grid'>\n"
        "<div class='score-card'><div class='score-label'>Overall Score</div>"
        "<div class='score-value'>" + str(overall_score) + "<span class='score-max'>/10</span></div>"
        "<div class='score-bar'><div class='score-fill' style='width:" + str(overall_score * 10) + "%;'></div></div>"
        "<div class='score-verdict'>" + data["overall_verdict"] + "</div></div>\n"
        "<div class='score-card'><div class='score-label'>CV Standout Score</div>"
        "<div class='score-value'>" + str(standout_score) + "<span class='score-max'>/10</span></div>"
        "<div class='score-bar'><div class='score-fill' style='width:" + str(standout_score * 10) + "%; background:#f59e0b;'></div></div>"
        "<div class='score-verdict'>" + data["cv_standout_verdict"] + "</div></div>\n"
        "<div class='score-card'><div class='score-label'>ATS Score</div>"
        "<div class='score-value'>" + str(ats_score) + "<span class='score-max'>/10</span></div>"
        "<div class='score-bar'><div class='score-fill' style='width:" + str(ats_score * 10) + "%; background:#3b82f6;'></div></div>"
        "<div class='score-verdict'>" + data["ats_verdict"] + "</div></div>\n"
        + jd_card +
        "</div>\n"
        "<div class='section'><h2>Strengths</h2><ul>" + strengths_li + "</ul></div>\n"
        "<div class='section'><h2>Weaknesses</h2><ul>" + weaknesses_li + "</ul></div>\n"
        "<div class='section'><h2>Missing Sections</h2><ul>" + missing_li + "</ul></div>\n"
        "<div class='section'><h2>Improvement Suggestions</h2><ul>" + suggestions_li + "</ul></div>\n"
        "<div class='section'><h2>Keyword Analysis</h2>"
        "<p style='font-size:0.85rem;color:#64748b;margin-bottom:10px;font-weight:600;'>PRESENT</p>"
        "<div>" + kw_present + "</div>"
        "<p style='font-size:0.85rem;color:#64748b;margin:14px 0 10px;font-weight:600;'>MISSING</p>"
        "<div>" + kw_missing + "</div></div>\n"
        "<div class='final'><h2>Final Recommendation</h2><p>" + data["final_recommendation"] + "</p></div>\n"
        "<div class='footer'>Resume Analyzer AI | Powered by Groq LLaMA 3.3</div>\n"
        "</div>\n</body>\n</html>"
    )


def safe_text(text):
    """Remove characters not supported by Helvetica/Latin-1"""
    replacements = {
        "\u2022": "-", "\u2013": "-", "\u2014": "-",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2026": "...", "\u00e9": "e", "\u00e8": "e", "\u00ea": "e",
        "\u00e0": "a", "\u00e2": "a", "\u00f9": "u", "\u00fb": "u",
        "\u00ee": "i", "\u00ef": "i", "\u00f4": "o", "\u00e7": "c",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def build_pdf_report(data, has_jd, resume_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    def cell(w, h, txt, bold=False, size=11, color=(15, 23, 42), align="L", ln=True):
        style = "B" if bold else ""
        pdf.set_font("Helvetica", style, size)
        pdf.set_text_color(*color)
        if ln:
            pdf.cell(w, h, safe_text(txt), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align=align)
        else:
            pdf.cell(w, h, safe_text(txt), align=align)

    def section_title(title):
        pdf.ln(4)
        cell(0, 10, title, bold=True, size=13)
        pdf.set_draw_color(226, 232, 240)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

    def score_row(label, score, verdict):
        cell(0, 7, label + ": " + str(score) + "/10", bold=True, size=11)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(0, 5, safe_text(verdict))
        pdf.ln(2)

    def list_items(items):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(51, 65, 85)
        for item in items:
            pdf.multi_cell(0, 6, safe_text("  - " + item))
            pdf.ln(1)

    # Title
    cell(0, 12, "Resume Analysis Report", bold=True, size=20)
    cell(0, 6, "File: " + resume_name + "  |  Resume Analyzer AI", size=10, color=(100, 116, 139))
    pdf.ln(4)

    # Scores
    section_title("Scores")
    score_row("Overall Score", data["overall_score"], data["overall_verdict"])
    score_row("CV Standout Score", data["cv_standout_score"], data["cv_standout_verdict"])
    score_row("ATS Score", data["ats_score"], data["ats_verdict"])
    if has_jd and "job_match_score" in data:
        score_row("Job Match Score", data["job_match_score"], data.get("job_match_verdict", ""))

    section_title("Strengths")
    list_items(data["strengths"])

    section_title("Weaknesses")
    list_items(data["weaknesses"])

    section_title("Missing Sections")
    list_items(data["missing_sections"])

    section_title("Improvement Suggestions")
    list_items(data["improvement_suggestions"])

    section_title("Keyword Analysis")
    cell(0, 6, "Present:", bold=True, size=10, color=(22, 101, 52))
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, safe_text("  " + ",  ".join(data["keywords_present"])))
    pdf.ln(3)
    cell(0, 6, "Missing:", bold=True, size=10, color=(153, 27, 27))
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, safe_text("  " + ",  ".join(data["keywords_missing"])))

    section_title("Final Recommendation")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, safe_text(data["final_recommendation"]))

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, "Resume Analyzer AI  |  Powered by Groq LLaMA 3.3", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return bytes(pdf.output())


# --- Streamlit UI ---
st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄", layout="wide")

st.title("📄 Resume Analyzer AI")
st.markdown("*Powered by Groq LLaMA 3.3*")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

job_desc = st.text_area(
    "📋 Job Description — paste here for job match scoring",
    height=180,
    placeholder="Paste the full job description here. The AI will rate how well your CV matches this role..."
)

analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

st.markdown("---")

if analyze_btn:
    if not uploaded_file:
        st.error("Please upload a resume first.")
    else:
        with st.spinner("Analyzing your resume..."):
            try:
                file_bytes = uploaded_file.read()
                if uploaded_file.name.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(file_bytes)
                else:
                    resume_text = extract_text_from_docx(file_bytes)

                if not resume_text.strip():
                    st.error("Could not extract text. Please try another file.")
                else:
                    has_jd = bool(job_desc.strip())
                    data = analyze_resume(resume_text, job_desc)

                    st.success("Analysis Complete!")

                    # Scores
                    st.subheader("📊 Scores")
                    num_cols = 4 if has_jd else 3
                    cols = st.columns(num_cols)
                    with cols[0]:
                        st.metric("Overall", f"{data['overall_score']}/10")
                        st.caption(data["overall_verdict"])
                    with cols[1]:
                        st.metric("CV Standout", f"{data['cv_standout_score']}/10")
                        st.caption(data["cv_standout_verdict"])
                    with cols[2]:
                        st.metric("ATS Score", f"{data['ats_score']}/10")
                        st.caption(data["ats_verdict"])
                    if has_jd:
                        with cols[3]:
                            st.metric("Job Match", f"{data['job_match_score']}/10")
                            st.caption(data["job_match_verdict"])

                    st.markdown("---")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.subheader("Strengths")
                        for s in data["strengths"]:
                            st.markdown(f"- {s}")
                    with col_b:
                        st.subheader("Weaknesses")
                        for w in data["weaknesses"]:
                            st.markdown(f"- {w}")

                    st.markdown("---")

                    col_c, col_d = st.columns(2)
                    with col_c:
                        st.subheader("Missing Sections")
                        for m in data["missing_sections"]:
                            st.markdown(f"- {m}")
                    with col_d:
                        st.subheader("Improvement Suggestions")
                        for i in data["improvement_suggestions"]:
                            st.markdown(f"- {i}")

                    st.markdown("---")

                    st.subheader("Keyword Analysis")
                    kc1, kc2 = st.columns(2)
                    with kc1:
                        st.markdown("**Present**")
                        st.markdown(" ".join([f"`{k}`" for k in data["keywords_present"]]))
                    with kc2:
                        st.markdown("**Missing**")
                        st.markdown(" ".join([f"`{k}`" for k in data["keywords_missing"]]))

                    st.markdown("---")

                    st.subheader("Final Recommendation")
                    st.info(data["final_recommendation"])

                    st.markdown("---")

                    st.subheader("Download Report")
                    dl1, dl2 = st.columns(2)
                    with dl1:
                        html_report = build_html_report(data, has_jd, uploaded_file.name)
                        st.download_button(
                            label="Download as HTML",
                            data=html_report,
                            file_name="resume_analysis_report.html",
                            mime="text/html",
                            use_container_width=True
                        )
                    with dl2:
                        pdf_report = build_pdf_report(data, has_jd, uploaded_file.name)
                        st.download_button(
                            label="Download as PDF",
                            data=pdf_report,
                            file_name="resume_analysis_report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.info("Upload your resume and optionally paste a job description, then click Analyze Resume.")
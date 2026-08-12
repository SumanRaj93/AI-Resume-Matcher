# AI Resume ↔ Job Matcher

AI-powered Resume ↔ Job Matching System built using Python, Flask, Scikit-learn, MySQL, Aiven, and Render.

This application compares a candidate's resume with a job description and generates an overall compatibility score based on ATS structure, skills, semantic similarity, experience, and education.

## 🚀 Live Demo

**Live Application:**  
https://ai-resume-matcher-vkev.onrender.com

**GitHub Repository:**  
https://github.com/SumanRaj93/AI-Resume-Matcher

---

## 📌 Features

- Resume upload in PDF and DOCX format
- ATS resume structure scoring
- Skill extraction and matching
- Semantic similarity using TF-IDF and Cosine Similarity
- Experience matching
- Education matching
- Missing skill identification
- Personalized recommendations
- Overall resume-job compatibility score
- Analytics dashboard
- Match history
- Anonymous session-based history
- Temporary resume file processing
- Cloud MySQL database using Aiven
- Production deployment using Render

---

## 🧠 How It Works

The application analyzes a resume through multiple stages:

```text
Resume
   ↓
PDF/DOCX Text Extraction
   ↓
ATS Analysis
   ↓
Skill Extraction
   ↓
Skill Matching
   ↓
Semantic Similarity
   ↓
Experience Matching
   ↓
Education Matching
   ↓
Final Compatibility Score
   ↓
Recommendations
   ↓
Dashboard & Match History

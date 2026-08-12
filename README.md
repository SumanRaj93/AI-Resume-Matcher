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
```

---

## 📊 Match Score Calculation

The final compatibility score is calculated using:

```text
Skill Match        → 50%
Semantic Match     → 25%
Experience Match   → 15%
Education Match    → 10%
```

### Formula

```text
Final Score =
    0.50 × Skill Score
  + 0.25 × Semantic Score
  + 0.15 × Experience Score
  + 0.10 × Education Score
```

### Recommendation Levels

```text
80 – 100%  → Strong Match
60 – 79%   → Moderate Match
0 – 59%    → Low Match
```

---

## 🤖 Semantic Similarity

The application uses **TF-IDF Vectorization** and **Cosine Similarity** to compare the resume with the job description.

```text
Resume Text
     +
Job Description
     ↓
TF-IDF Vectorization
     ↓
Cosine Similarity
     ↓
Semantic Match Score
```

TF-IDF was chosen instead of a large transformer model to keep the application lightweight and suitable for low-memory cloud deployment.

The initial version used Sentence Transformers, but the model required significantly more memory during deployment. Replacing it with TF-IDF and Cosine Similarity allowed the application to run successfully on the Render Free environment.

---

## 🛠️ Skill Matching

The application extracts skills from both the resume and job description and compares them.

Example:

```text
Resume Skills:
Python
SQL
Power BI
Excel
Pandas

Job Skills:
Python
SQL
Power BI
Excel
Pandas
Tableau
```

The system identifies:

```text
Matched Skills:
Python
SQL
Power BI
Excel
Pandas

Missing Skills:
Tableau
```

The skill score is calculated based on the percentage of required job skills found in the resume.

---

## 💼 Experience Matching

The application analyzes the resume and job description to estimate experience compatibility.

It considers:

- Required experience
- Resume experience
- Experience compatibility

Experience contributes **15%** to the final compatibility score.

---

## 🎓 Education Matching

The application compares education information from the resume with the education requirements of the job description.

Education contributes **10%** to the final compatibility score.

---

## 💡 Recommendations

The application identifies skills required by the job that are missing from the resume.

Example:

```text
Missing Skills:
- Tableau
- ETL
- Data Warehousing
```

These recommendations help candidates identify areas where they can improve their skills or resume.

---

## 📈 Dashboard

The application provides an analytics dashboard containing:

- Total analyses
- Average match score
- Best match
- Strong matches
- Match score by job
- Recent analyses

The dashboard allows users to compare their resume compatibility across different job roles.

---

## 🕒 Match History

Previous resume-job analysis results are stored in MySQL.

Users can view:

- Resume name
- Job title
- Match score
- Recommendation
- Analysis date

---

## 🔐 Privacy

The application uses anonymous browser sessions.

Each browser receives a unique anonymous session ID, and dashboard/history results are associated with that session.

### Resume Handling

Uploaded resumes:

- Receive unique temporary filenames
- Are processed only for text extraction
- Are deleted after processing
- Are not stored as PDF/DOCX files in MySQL

The database stores analysis results rather than the uploaded resume files.

> This is an anonymous demo application and does not include a full user authentication system.

---

## 🛠️ Technology Stack

### Backend

- Python
- Flask
- Gunicorn

### Machine Learning / NLP

- Scikit-learn
- TF-IDF
- Cosine Similarity

### Resume Processing

- PyMuPDF
- python-docx

### Database

- MySQL
- Aiven MySQL

### Frontend

- HTML
- CSS
- JavaScript

### Development

- VS Code
- Git
- GitHub

### Deployment

- Render
- Aiven

---

## 📂 Project Structure

```text
AI-Resume-Matcher/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── semantic_matcher.py
│   ├── skill_extractor.py
│   ├── profile_extractor.py
│   ├── ats_analyzer.py
│   ├── recommendations.py
│   │
│   ├── static/
│   │   └── style.css
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── result.html
│   │   ├── dashboard.html
│   │   └── history.html
│   │
│   └── uploads/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SumanRaj93/AI-Resume-Matcher.git
cd AI-Resume-Matcher
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

For local development, configure the following environment variables:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=resume_matcher
FLASK_SECRET_KEY=your_secret_key
```

### Create the Database

Open MySQL and run:

```sql
CREATE DATABASE resume_matcher;
```

The application automatically creates the required `match_results` table.

---

## ▶️ Run Locally

Move into the backend directory:

```bash
cd backend
```

Run the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🌐 Production Deployment

The application is deployed using:

```text
GitHub
   ↓
Render
   ↓
Flask + Gunicorn
   ↓
Aiven MySQL
```

### Render Configuration

**Root Directory**

```text
backend
```

**Build Command**

```bash
pip install -r ../requirements.txt
```

**Start Command**

```bash
gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
```

---

## 🔑 Environment Variables

The deployed application uses:

```text
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_NAME
FLASK_SECRET_KEY
```

Sensitive credentials should never be committed to GitHub.

---

## 🗄️ Aiven MySQL

The deployed application uses Aiven MySQL as its cloud database.

The `match_results` table stores:

```text
Session ID
Resume Name
Job Title
ATS Score
Skill Score
Semantic Score
Experience Score
Education Score
Final Score
Recommendation
Created At
```

Uploaded resume files themselves are not stored in the database.

---

## 📊 Example Result

A typical analysis produces results such as:

```text
ATS Score:        92%
Skill Score:      84%
Semantic Score:   79%
Experience Score: 80%
Education Score:  100%

Final Match:      84.55%

Recommendation:   Strong Match
```

The actual score depends on the resume and job description provided by the user.

---

## 🎯 Example Use Case

A candidate applying for a **Business Intelligence Analyst** role can upload their resume and provide the job description.

The system can identify:

```text
Matched Skills:
SQL
Python
Power BI
Excel
Pandas

Missing Skills:
Tableau
ETL
Data Warehousing
```

The candidate can use the results to understand their compatibility with the position and identify skills that may need improvement.

---

## 🚀 Future Improvements

- User registration and authentication
- Multiple resume profiles
- Resume improvement suggestions
- Automated resume keyword optimization
- Job recommendation system
- LinkedIn/job portal integration
- Advanced NLP models
- Recruiter dashboard
- Resume version comparison
- PDF report generation
- REST API
- Advanced analytics
- Batch resume processing

---

## 👨‍💻 Author

**Suman Raj**

B.Tech Computer Science & Engineering (AI & ML)

**GitHub:**  
https://github.com/SumanRaj93/AI-Resume-Matcher

---

## 🌐 Live Application

Try the application:

https://ai-resume-matcher-vkev.onrender.com

---

## ⭐ Project Highlights

This project demonstrates practical experience with:

- Python
- Flask
- Machine Learning
- Natural Language Processing
- Scikit-learn
- TF-IDF
- Cosine Similarity
- SQL
- MySQL
- Cloud Database Integration
- Git
- GitHub
- Render Deployment
- Application Optimization
- Production Deployment

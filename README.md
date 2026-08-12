# AI Resume ↔ Job Matcher

A Flask application that compares a resume with a job description using:
- ATS structure scoring
- skill matching
- SentenceTransformer semantic similarity
- experience matching
- education matching
- recommendations

## Important privacy behavior

The public-ready version:
- gives each browser a unique anonymous session ID
- shows dashboard/history only for that session
- gives uploaded files unique temporary names
- deletes uploaded resumes after text extraction
- does not store the resume PDF/DOCX in MySQL

This is an anonymous session-based demo, not a full account system. For a production SaaS, add user authentication and stronger session/security controls.

## Setup

Create a virtual environment and install:

```bash
pip install -r requirements.txt
```

Set these environment variables before starting:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=resume_matcher
FLASK_SECRET_KEY=replace-with-a-long-random-secret
```

Create the MySQL database:

```sql
CREATE DATABASE resume_matcher;
```

The application creates the `match_results` table automatically.

Run:

```bash
cd backend
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Deployment

Use a production WSGI server such as Gunicorn:

```bash
gunicorn --chdir backend app:app
```

Configure an external MySQL database and environment variables on your hosting platform.

Do not commit `.env`, passwords, resumes, or `venv/` to GitHub.

from flask import Flask, render_template, request, session
import os
import uuid
from pathlib import Path

import pymupdf
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from skill_extractor import extract_skills
from profile_extractor import calculate_experience_score, calculate_education_score
from ats_analyzer import calculate_ats_score
from recommendations import generate_recommendations
from database import get_connection, ensure_schema


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-in-production")
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


print("Loading AI model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("AI model loaded successfully.")


def get_session_id():
    if "user_id" not in session:
        session["user_id"] = uuid.uuid4().hex
        session.permanent = True
    return session["user_id"]


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def extract_text(file_path, extension):
    if extension == "pdf":
        document = pymupdf.open(str(file_path))
        try:
            return "\n".join(page.get_text() for page in document)
        finally:
            document.close()

    if extension == "docx":
        from docx import Document
        document = Document(str(file_path))
        return "\n".join(p.text for p in document.paragraphs)

    raise ValueError("Unsupported file type.")


def clamp_score(value):
    return max(0.0, min(100.0, float(value)))


def save_result(session_id, values):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO match_results
        (
            session_id, resume_name, job_title, ats_score,
            skill_score, semantic_score, experience_score,
            education_score, final_score, recommendation
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        session_id,
        values["resume_name"],
        values["job_title"],
        values["ats_score"],
        values["skill_score"],
        values["semantic_score"],
        values["experience_score"],
        values["education_score"],
        values["final_score"],
        values["recommendation"],
    ))

    connection.commit()
    cursor.close()
    connection.close()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files.get("resume")
    job_text = request.form.get("job_description", "").strip()

    if not resume or not resume.filename:
        return render_template("index.html", error="Please select a resume file."), 400

    if not allowed_file(resume.filename):
        return render_template(
            "index.html",
            error="Only PDF and DOCX resumes are supported."
        ), 400

    if not job_text:
        return render_template(
            "index.html",
            error="Please enter a job description."
        ), 400

    original_name = secure_filename(resume.filename)
    extension = original_name.rsplit(".", 1)[1].lower()

    # Unique temporary filename prevents collisions between users.
    temp_name = f"{uuid.uuid4().hex}.{extension}"
    resume_path = UPLOAD_FOLDER / temp_name

    try:
        resume.save(resume_path)
        resume_text = extract_text(resume_path, extension)
    except Exception as exc:
        return render_template(
            "index.html",
            error=f"Could not read the resume: {exc}"
        ), 400
    finally:
        # Do not retain users' resumes on the server.
        try:
            resume_path.unlink(missing_ok=True)
        except Exception:
            pass

    if not resume_text.strip():
        return render_template(
            "index.html",
            error="Could not extract text from the resume."
        ), 400

    ats_score, ats_sections = calculate_ats_score(resume_text)

    resume_skill_set = set(extract_skills(resume_text))
    job_skill_set = set(extract_skills(job_text))

    matched_skills = resume_skill_set.intersection(job_skill_set)
    missing_skills = job_skill_set.difference(resume_skill_set)

    skill_score = (
        (len(matched_skills) / len(job_skill_set)) * 100
        if job_skill_set else 0
    )

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])

    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
    semantic_score = clamp_score(similarity * 100)

    experience_score, required_years, resume_years = calculate_experience_score(
        resume_text, job_text
    )
    education_score = calculate_education_score(resume_text, job_text)

    final_score = clamp_score(
        0.50 * skill_score
        + 0.25 * semantic_score
        + 0.15 * experience_score
        + 0.10 * education_score
    )

    if final_score >= 80:
        recommendation, recommendation_icon = "Strong Match", "🟢"
    elif final_score >= 60:
        recommendation, recommendation_icon = "Moderate Match", "🟡"
    else:
        recommendation, recommendation_icon = "Low Match", "🔴"

    job_title = job_text.splitlines()[0].strip()[:255] or "Job Description"

    values = {
        "resume_name": original_name[:255],
        "job_title": job_title,
        "ats_score": round(float(ats_score), 2),
        "skill_score": round(float(skill_score), 2),
        "semantic_score": round(float(semantic_score), 2),
        "experience_score": round(float(experience_score), 2),
        "education_score": round(float(education_score), 2),
        "final_score": round(float(final_score), 2),
        "recommendation": recommendation,
    }

    try:
        ensure_schema()
        save_result(get_session_id(), values)
    except Exception as exc:
        # Analysis still works even if MySQL is temporarily unavailable.
        print("Database Error:", exc)

    return render_template(
        "result.html",
        final_score=values["final_score"],
        ats_score=values["ats_score"],
        ats_sections=ats_sections,
        skill_score=values["skill_score"],
        semantic_score=values["semantic_score"],
        experience_score=values["experience_score"],
        education_score=values["education_score"],
        recommendation=recommendation,
        recommendation_icon=recommendation_icon,
        recommendations=generate_recommendations(sorted(missing_skills)),
        required_years=required_years,
        resume_years=resume_years,
        matched_skills=sorted(matched_skills),
        missing_skills=sorted(missing_skills),
    )


def get_user_results():
    ensure_schema()
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT *
        FROM match_results
        WHERE session_id = %s
        ORDER BY created_at DESC
        """,
        (get_session_id(),)
    )
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


@app.route("/dashboard")
def dashboard():
    results = get_user_results()

    total_analyses = len(results)
    scores = [float(row["final_score"]) for row in results]
    average_score = round(sum(scores) / len(scores), 2) if scores else 0
    best_score = round(max(scores), 2) if scores else 0
    strong_matches = sum(score >= 80 for score in scores)
    best_match = max(results, key=lambda row: float(row["final_score"])) if results else None

    # Add a unique short label so different companies/jobs don't all look identical.
    chart_labels = []
    seen_titles = {}
    for row in results[:10]:
        title = (row["job_title"] or "Job")[:24]
        seen_titles[title] = seen_titles.get(title, 0) + 1
        count = seen_titles[title]
        chart_labels.append(f"{title}" if count == 1 else f"{title} #{count}")
    chart_scores = [float(row["final_score"]) for row in results[:10]]

    return render_template(
        "dashboard.html",
        results=results,
        total_analyses=total_analyses,
        average_score=average_score,
        best_score=best_score,
        strong_matches=strong_matches,
        best_match=best_match,
        chart_labels=chart_labels,
        chart_scores=chart_scores,
    )


@app.route("/history")
def history():
    return render_template("history.html", results=get_user_results())


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5000")),
        debug=False,
        use_reloader=False
    )
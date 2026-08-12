def calculate_ats_score(resume_text):

    text = resume_text.lower()

    score = 0

    checks = {
        "skills": [
            "python",
            "sql",
            "java"
        ],

        "projects": [
            "project",
            "projects"
        ],

        "education": [
            "education",
            "b.tech",
            "btech",
            "degree"
        ],

        "experience": [
            "experience",
            "internship",
            "intern"
        ],

        "certifications": [
            "certification",
            "certificate"
        ]
    }

    section_scores = {}

    # Skills
    if any(word in text for word in checks["skills"]):
        score += 20
        section_scores["Skills"] = 20
    else:
        section_scores["Skills"] = 0

    # Projects
    if any(word in text for word in checks["projects"]):
        score += 20
        section_scores["Projects"] = 20
    else:
        section_scores["Projects"] = 0

    # Education
    if any(word in text for word in checks["education"]):
        score += 20
        section_scores["Education"] = 20
    else:
        section_scores["Education"] = 0

    # Experience
    if any(word in text for word in checks["experience"]):
        score += 20
        section_scores["Experience"] = 20
    else:
        section_scores["Experience"] = 0

    # Certifications
    if any(word in text for word in checks["certifications"]):
        score += 20
        section_scores["Certifications"] = 20
    else:
        section_scores["Certifications"] = 0

    return score, section_scores
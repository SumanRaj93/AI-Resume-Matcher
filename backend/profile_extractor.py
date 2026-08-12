import re


def extract_required_experience(job_text):

    pattern = r'(\d+)\+?\s*(?:years?|yrs?)'

    matches = re.findall(
        pattern,
        job_text.lower()
    )

    if matches:
        return max(int(year) for year in matches)

    return 0


def extract_resume_experience(resume_text):

    text = resume_text.lower()

    # Look for explicit experience statements
    pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience'

    matches = re.findall(pattern, text)

    if matches:
        return max(int(year) for year in matches)

    # Internship / work experience detection
    experience_keywords = [
        "internship",
        "intern",
        "work experience",
        "professional experience",
        "employment"
    ]

    for keyword in experience_keywords:
        if keyword in text:
            return 1

    return 0


def calculate_experience_score(
    resume_text,
    job_text
):

    required_years = extract_required_experience(
        job_text
    )

    resume_years = extract_resume_experience(
        resume_text
    )

    # If job doesn't specify experience,
    # don't penalize the candidate.
    if required_years == 0:
        score = 100

    elif resume_years >= required_years:
        score = 100

    elif resume_years > 0:
        score = 50

    else:
        score = 0

    return score, required_years, resume_years


def calculate_education_score(
    resume_text,
    job_text
):

    resume = resume_text.lower()
    job = job_text.lower()

    education_terms = [
        "b.tech",
        "btech",
        "b.e",
        "bachelor",
        "computer science",
        "engineering",
        "master",
        "m.tech",
        "mtech",
        "mba",
        "degree"
    ]

    job_has_education_requirement = any(
        term in job
        for term in education_terms
    )

    resume_has_education = any(
        term in resume
        for term in education_terms
    )

    # No education requirement in job
    if not job_has_education_requirement:
        return 100

    # Job asks for education and resume contains
    # education information
    if resume_has_education:
        return 100

    return 0
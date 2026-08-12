import pymupdf
from skill_extractor import extract_skills


# --------------------------------
# 1. Extract skills from resume
# --------------------------------

pdf_path = "uploads/Resume .pdf"

document = pymupdf.open(pdf_path)

resume_text = ""

for page in document:
    resume_text += page.get_text()

document.close()

resume_skills = extract_skills(resume_text)


# --------------------------------
# 2. Read job description
# --------------------------------

with open("job_description.txt", "r", encoding="utf-8") as file:
    job_text = file.read()

job_skills = extract_skills(job_text)


# --------------------------------
# 3. Convert skills into sets
# --------------------------------

resume_skills = set(resume_skills)
job_skills = set(job_skills)


# --------------------------------
# 4. Find matching skills
# --------------------------------

matched_skills = resume_skills.intersection(job_skills)


# --------------------------------
# 5. Find missing skills
# --------------------------------

missing_skills = job_skills.difference(resume_skills)


# --------------------------------
# 6. Calculate match score
# --------------------------------

if len(job_skills) > 0:
    match_score = (len(matched_skills) / len(job_skills)) * 100
else:
    match_score = 0


# --------------------------------
# 7. Display results
# --------------------------------

print("\n==============================")
print("      AI RESUME MATCHER")
print("==============================")

print("\nResume Skills:")
for skill in sorted(resume_skills):
    print("✓", skill)

print("\nJob Skills:")
for skill in sorted(job_skills):
    print("•", skill)

print("\nMatched Skills:")
for skill in sorted(matched_skills):
    print("✓", skill)

print("\nMissing Skills:")
for skill in sorted(missing_skills):
    print("✗", skill)

print("\n==============================")
print("MATCH SCORE:", round(match_score, 2), "%")
print("==============================")
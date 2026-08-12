import pymupdf

from skill_extractor import extract_skills

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. READ RESUME
# ==========================================

pdf_path = "uploads/Resume .pdf"

document = pymupdf.open(pdf_path)

resume_text = ""

for page in document:
    resume_text += page.get_text()

document.close()


# ==========================================
# 2. EXTRACT RESUME SKILLS
# ==========================================

resume_skills = extract_skills(resume_text)


# ==========================================
# 3. READ JOB DESCRIPTION
# ==========================================

with open("job_description.txt", "r", encoding="utf-8") as file:
    job_text = file.read()


# ==========================================
# 4. EXTRACT JOB SKILLS
# ==========================================

job_skills = extract_skills(job_text)


# ==========================================
# 5. SKILL MATCHING
# ==========================================

resume_skill_set = set(resume_skills)

job_skill_set = set(job_skills)

matched_skills = resume_skill_set.intersection(job_skill_set)

missing_skills = job_skill_set.difference(resume_skill_set)


if len(job_skill_set) > 0:

    skill_match_score = (
        len(matched_skills) / len(job_skill_set)
    ) * 100

else:

    skill_match_score = 0


# ==========================================
# 6. SEMANTIC AI MATCHING
# ==========================================

model = SentenceTransformer("all-MiniLM-L6-v2")


resume_embedding = model.encode([resume_text])

job_embedding = model.encode([job_text])


similarity = cosine_similarity(
    resume_embedding,
    job_embedding
)


semantic_score = similarity[0][0] * 100


# ==========================================
# 7. FINAL SCORE
# ==========================================

final_score = (
    0.60 * skill_match_score
    + 0.40 * semantic_score
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n===================================")
print("       AI RESUME ↔ JOB MATCHER")
print("===================================")

print("\nResume Skills:")

for skill in sorted(resume_skill_set):
    print("✓", skill)


print("\nJob Skills:")

for skill in sorted(job_skill_set):
    print("•", skill)


print("\nMatched Skills:")

for skill in sorted(matched_skills):
    print("✓", skill)


print("\nMissing Skills:")

for skill in sorted(missing_skills):
    print("✗", skill)


print("\n-----------------------------------")

print(
    "Skill Match:",
    round(skill_match_score, 2),
    "%"
)

print(
    "Semantic Match:",
    round(semantic_score, 2),
    "%"
)

print(
    "FINAL MATCH SCORE:",
    round(final_score, 2),
    "%"
)

print("-----------------------------------")
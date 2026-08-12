import pymupdf
from skill_extractor import extract_skills

pdf_path = "uploads/Resume .pdf"

document = pymupdf.open(pdf_path)

text = ""

for page in document:
    text += page.get_text()

document.close()

print("----- RESUME TEXT -----")
print(text)

print("\n----- DETECTED SKILLS -----")

skills = extract_skills(text)

for skill in skills:
    print("✓", skill)
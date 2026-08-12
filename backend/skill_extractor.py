def extract_skills(text):

    skills = [
        "python",
        "java",
        "sql",
        "mysql",
        "mongodb",
        "power bi",
        "power query",
        "excel",
        "dax",
        "pandas",
        "numpy",
        "scikit-learn",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "flask",
        "git",
        "github",
        "smote",
        "tableau",
"data visualization",
"communication",
"data analysis"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return found_skills
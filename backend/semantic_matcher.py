from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


resume_text = """
Created interactive business intelligence dashboards
using Power BI and analyzed employee data.
"""


job_text = """
Experience in Power BI dashboards and business data analysis.
"""


resume_embedding = model.encode([resume_text])
job_embedding = model.encode([job_text])


similarity = cosine_similarity(
    resume_embedding,
    job_embedding
)


score = similarity[0][0] * 100


print("Semantic Similarity:", round(score, 2), "%")
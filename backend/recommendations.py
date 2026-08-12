def generate_recommendations(missing_skills):

    recommendations = []

    skill_advice = {

        "python":
            "Improve Python programming and data analysis skills.",

        "sql":
            "Practice SQL joins, subqueries, aggregation and window functions.",

        "excel":
            "Improve Excel skills including Pivot Tables, formulas and data cleaning.",

        "power bi":
            "Build Power BI dashboards and practice DAX and Power Query.",

        "tableau":
            "Create at least one Tableau dashboard project.",

        "data visualization":
            "Practice creating charts, dashboards and business visualizations.",

        "machine learning":
            "Build an ML project and demonstrate model evaluation techniques.",

        "pandas":
            "Practice data cleaning, transformation and analysis using Pandas.",

        "numpy":
            "Practice numerical analysis and array operations using NumPy.",

        "mongodb":
            "Practice document-based database design and MongoDB queries.",

        "java":
            "Strengthen Java OOP, collections and problem-solving skills."

    }


    for skill in missing_skills:

        if skill in skill_advice:

            recommendations.append(
                skill_advice[skill]
            )

        else:

            recommendations.append(
                f"Learn and add practical experience with {skill}."
            )


    return recommendations
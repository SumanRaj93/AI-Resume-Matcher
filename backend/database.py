import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "resume_matcher"),
        port=int(os.getenv("DB_PORT", "3306")),
    )


def ensure_schema():
    """Create the results table if needed and add session_id for privacy."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(64) NOT NULL,
            resume_name VARCHAR(255) NOT NULL,
            job_title VARCHAR(255) NOT NULL,
            ats_score DECIMAL(6,2) NOT NULL,
            skill_score DECIMAL(6,2) NOT NULL,
            semantic_score DECIMAL(6,2) NOT NULL,
            experience_score DECIMAL(6,2) NOT NULL,
            education_score DECIMAL(6,2) NOT NULL,
            final_score DECIMAL(6,2) NOT NULL,
            recommendation VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Supports an existing table from the original local project.
    cursor.execute("SHOW COLUMNS FROM match_results LIKE 'session_id'")
    if cursor.fetchone() is None:
        cursor.execute(
            "ALTER TABLE match_results "
            "ADD COLUMN session_id VARCHAR(64) NULL"
        )
        cursor.execute(
            "UPDATE match_results SET session_id = 'legacy-local-data' "
            "WHERE session_id IS NULL"
        )

    connection.commit()
    cursor.close()
    connection.close()

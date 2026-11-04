from pathlib import Path
import sqlite3


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "moderation.db"
)


def initialize_database():
    """
    Create the moderation database and results table if they do not exist.
    """

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS moderation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_text TEXT NOT NULL,
            toxic REAL NOT NULL,
            severe_toxic REAL NOT NULL,
            obscene REAL NOT NULL,
            threat REAL NOT NULL,
            insult REAL NOT NULL,
            identity_hate REAL NOT NULL,
            recommended_action TEXT NOT NULL,
            moderator_action TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()

def save_moderation_result(comment_text, probabilities, recommended_action):
    """
    Save one analyzed comment and its moderation result to the database.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO moderation_results (
            comment_text,
            toxic,
            severe_toxic,
            obscene,
            threat,
            insult,
            identity_hate,
            recommended_action
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            comment_text,
            probabilities["toxic"],
            probabilities["severe_toxic"],
            probabilities["obscene"],
            probabilities["threat"],
            probabilities["insult"],
            probabilities["identity_hate"],
            recommended_action
        )
    )

    connection.commit()
    connection.close()
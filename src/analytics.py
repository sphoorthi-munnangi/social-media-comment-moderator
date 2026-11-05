import sqlite3

from src.database import DATABASE_PATH


def get_action_counts():
    """
    Count comments by model-recommended moderation action.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    rows = connection.execute(
        """
        SELECT recommended_action, COUNT(*)
        FROM moderation_results
        GROUP BY recommended_action
        """
    ).fetchall()

    connection.close()

    return dict(rows)

def get_total_comments():
    """
    Return the total number of comments analyzed.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    total = connection.execute(
        """
        SELECT COUNT(*)
        FROM moderation_results
        """
    ).fetchone()[0]

    connection.close()

    return total

def get_moderator_action_counts():
    """
    Count saved human moderator decisions.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    rows = connection.execute(
        """
        SELECT moderator_action, COUNT(*)
        FROM moderation_results
        WHERE moderator_action IS NOT NULL
        GROUP BY moderator_action
        """
    ).fetchall()

    connection.close()

    return dict(rows)
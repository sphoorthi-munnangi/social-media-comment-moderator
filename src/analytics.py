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

def get_flagged_rate():
    """
    Return the percentage of analyzed comments that require moderator attention.
    """

    total = get_total_comments()

    if total == 0:
        return 0.0

    action_counts = get_action_counts()

    flagged = (
        action_counts.get("REVIEW", 0)
        + action_counts.get("HIDE_CANDIDATE", 0)
    )

    return (flagged / total) * 100


def get_auto_allow_rate():
    """
    Return the percentage of comments automatically recommended as ALLOW.
    """

    total = get_total_comments()

    if total == 0:
        return 0.0

    action_counts = get_action_counts()
    allowed = action_counts.get("ALLOW", 0)

    return (allowed / total) * 100

def get_review_completion_rate():
    """
    Return the percentage of flagged comments that received
    a human moderator decision.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    flagged = connection.execute(
        """
        SELECT COUNT(*)
        FROM moderation_results
        WHERE recommended_action IN ('REVIEW', 'HIDE_CANDIDATE')
        """
    ).fetchone()[0]

    completed = connection.execute(
        """
        SELECT COUNT(*)
        FROM moderation_results
        WHERE recommended_action IN ('REVIEW', 'HIDE_CANDIDATE')
          AND moderator_action IS NOT NULL
        """
    ).fetchone()[0]

    connection.close()

    if flagged == 0:
        return 0.0

    return (completed / flagged) * 100

def get_recent_results(limit=10):
    """
    Return the most recent moderation records.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT
            comment_text,
            recommended_action,
            moderator_action,
            created_at
        FROM moderation_results
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]
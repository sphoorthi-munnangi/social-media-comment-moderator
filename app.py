import streamlit as st

from src.comment_analyzer import analyze_comment
from src.database import (
    initialize_database,
    save_moderation_result,
    update_moderator_action
)

from src.analytics import (
    get_action_counts,
    get_moderator_action_counts,
    get_total_comments
)

initialize_database()


st.title("Social Media Comment Moderator")

st.write(
    "Analyze a social media comment for potentially harmful content "
    "and receive a moderation recommendation."
)

comment = st.text_area(
    "Enter a comment:",
    placeholder="Type or paste a social media comment here..."
)

if st.button("Analyze Comment"):
    if comment.strip():
        with st.spinner("Analyzing comment..."):
            result = analyze_comment(comment)

        action = result["action"]
        probabilities = result["probabilities"]

        record_id = save_moderation_result(
            comment,
            probabilities,
            action
        )

        st.session_state["record_id"] = record_id
        st.session_state["probabilities"] = probabilities
        st.session_state["action"] = action
        st.session_state["comment"] = comment
        st.session_state["moderator_action"] = None

    else:
        st.warning("Please enter a comment before analyzing.")


if "record_id" in st.session_state:
    action = st.session_state["action"]
    probabilities = st.session_state["probabilities"]
    analyzed_comment = st.session_state["comment"]

    st.subheader("Moderation Recommendation")

    if action == "ALLOW":
        st.success("ALLOW — No harmful content detected.")
    elif action == "REVIEW":
        st.warning(
            "REVIEW — This comment should be reviewed by a moderator."
        )
    else:
        st.error(
            "HIDE CANDIDATE — High-confidence harmful content detected."
        )

    st.caption(f'Analyzed comment: "{analyzed_comment}"')

    st.subheader("Content Risk Scores")

    for label, probability in probabilities.items():
        display_label = label.replace("_", " ").title()
        st.write(f"{display_label}: {probability:.1%}")
        st.progress(probability)

    if action != "ALLOW":
        st.subheader("Moderator Decision")

        allow_column, hide_column = st.columns(2)

        with allow_column:
            if st.button("Allow Comment"):
                update_moderator_action(
                    st.session_state["record_id"],
                    "ALLOW"
                )
                st.session_state["moderator_action"] = "ALLOW"

        with hide_column:
            if st.button("Hide Comment"):
                update_moderator_action(
                    st.session_state["record_id"],
                    "HIDE"
                )
                st.session_state["moderator_action"] = "HIDE"

        if st.session_state["moderator_action"]:
            st.info(
                "Moderator decision saved: "
                f"{st.session_state['moderator_action']}"
            )

st.divider()

st.header("Moderation Analytics")

total_comments = get_total_comments()
action_counts = get_action_counts()
moderator_counts = get_moderator_action_counts()

flagged_comments = (
    action_counts.get("REVIEW", 0)
    + action_counts.get("HIDE_CANDIDATE", 0)
)

human_decisions = sum(moderator_counts.values())

column1, column2, column3 = st.columns(3)

column1.metric("Total Comments", total_comments)
column2.metric("Model Flagged", flagged_comments)
column3.metric("Human Decisions", human_decisions)

st.subheader("Model Recommendation Distribution")

recommendation_data = {
    "Allow": action_counts.get("ALLOW", 0),
    "Review": action_counts.get("REVIEW", 0),
    "Hide Candidate": action_counts.get("HIDE_CANDIDATE", 0)
}

st.bar_chart(
    recommendation_data,
    horizontal=True
)

st.caption(
    "Current analytics are based on development and test comments "
    "stored in the local database."
)
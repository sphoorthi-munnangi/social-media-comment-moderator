import streamlit as st

from src.comment_analyzer import analyze_comment


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

        st.subheader("Content Risk Scores")

        for label, probability in probabilities.items():
            display_label = label.replace("_", " ").title()
            st.write(f"{display_label}: {probability:.1%}")
            st.progress(probability)

    else:
        st.warning("Please enter a comment before analyzing.")
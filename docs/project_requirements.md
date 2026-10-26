# Social Media Comment Moderator — Project Requirements

## 1. Business Problem

Social media users, creators, and organizations may receive large numbers of comments across their posts. Manually reviewing every comment can be time-consuming, while automatically removing comments without sufficient confidence can result in legitimate content being incorrectly moderated.

The goal of this project is to develop a data-driven moderation application that identifies potentially harmful comments and helps users determine whether those comments should be allowed, reviewed, or hidden.

## 2. Project Objective

Build an application that can:

- Analyze social media comments for potentially harmful content.
- Assign risk or toxicity scores to comments.
- Recommend a moderation action.
- Allow a human user to review and override recommendations.
- Store moderation results for future analysis.
- Provide analytics about comment activity and moderation performance.
- Eventually connect to authorized social media accounts through official APIs.

## 3. Initial Moderation Decisions

The system will assign comments to one of three moderation outcomes:

- **ALLOW** — The comment is considered low risk and remains visible.
- **REVIEW** — The system is uncertain or the comment requires human judgment.
- **HIDE** — The comment is considered high risk and is recommended for removal from public view.

## 4. Initial Harmful Content Categories

The first version of the model will focus on detecting:

- Toxic content
- Severe toxicity
- Insults
- Threats
- Obscene content
- Identity-based attacks

Additional categories such as spam or scams may be added later.

## 5. Human-in-the-Loop Principle

The system will not assume that the machine-learning model is always correct. Users will be able to review flagged comments and override the model's recommendation.

These decisions can later be analyzed to identify false positives, false negatives, and opportunities to improve the moderation system.

## 6. Functional Requirements

The application should be able to:

1. Accept individual comment text for analysis.
2. Analyze comments for different categories of harmful content.
3. Generate a score indicating the likelihood of each harmful-content category.
4. Recommend one of three moderation actions: **ALLOW, REVIEW, or HIDE**.
5. Allow the user to override the system's recommended action.
6. Store analyzed comments, model scores, recommendations, and final moderation decisions.
7. Display analytics summarizing comment activity and moderation results.
8. Eventually retrieve comments from authorized social media accounts through official APIs.
9. Eventually perform permitted moderation actions, such as hiding or rejecting comments, through those APIs.

## 7. Success Metrics

The system will be evaluated using both machine-learning and business-oriented metrics.

### Model Performance Metrics

- Precision
- Recall
- F1 Score
- False-positive rate
- False-negative rate

### Moderation and Business Metrics

- Percentage of comments classified as low, medium, and high risk
- Percentage of comments automatically handled
- Percentage of comments requiring human review
- Human agreement rate with model recommendations
- Number and percentage of model recommendations overridden by the user
- Estimated reduction in comments requiring manual moderation

Specific performance targets will be determined after a baseline model has been developed and evaluated.
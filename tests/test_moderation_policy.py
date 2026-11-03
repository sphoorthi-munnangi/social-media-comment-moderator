import unittest

from src.moderation_policy import get_moderation_action


class TestModerationPolicy(unittest.TestCase):

    def test_allow(self):
        probabilities = {
            "toxic": 0.05,
            "severe_toxic": 0.01,
            "obscene": 0.03,
            "threat": 0.01,
            "insult": 0.04,
            "identity_hate": 0.01
        }

        self.assertEqual(
            get_moderation_action(probabilities),
            "ALLOW"
        )

    def test_review(self):
        probabilities = {
            "toxic": 0.72,
            "severe_toxic": 0.03,
            "obscene": 0.15,
            "threat": 0.02,
            "insult": 0.30,
            "identity_hate": 0.01
        }

        self.assertEqual(
            get_moderation_action(probabilities),
            "REVIEW"
        )

    def test_hide_candidate(self):
        probabilities = {
            "toxic": 0.96,
            "severe_toxic": 0.10,
            "obscene": 0.82,
            "threat": 0.05,
            "insult": 0.88,
            "identity_hate": 0.03
        }

        self.assertEqual(
            get_moderation_action(probabilities),
            "HIDE_CANDIDATE"
        )


if __name__ == "__main__":
    unittest.main()
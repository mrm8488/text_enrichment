import unittest
from enricher import Enricher

# Assuming we have a mock model for testing purposes


class ZSTopicMockModel:
    def predict(self, text, lang):
        return {"topic": "AI"}


class TestEnricher(unittest.TestCase):

    def setUp(self):
        # Set up data and instances that will be used across multiple tests
        self.enricher = Enricher(models=["zs_topic"])
        self.enricher.models = {"zs_topic": ZSTopicMockModel()}  # Mocking the model

    def test_initialize_with_models(self):
        self.assertIn("zs_topic", self.enricher.models)

    def test_process_text(self):
        # Mock input
        text_input = "This is a sample text talking about AI."

        # Expected output
        expected_output = {"topic": "AI"}

        # Actual output
        result = self.enricher.process(text_input)

        # Assert that the result matches our expected output
        self.assertEqual(result, expected_output)

    def test_empty_input(self):
        text_input = ""
        expected_output = {}
        result = self.enricher.process(text_input)
        self.assertEqual(result, expected_output)

    # Add more tests as needed...


if __name__ == "__main__":
    unittest.main()

from transformers import pipeline
from models.base import Model

model_id = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
default_candidate_labels = ["politics",
                            "economy", "entertainment", "environment", "science", "biology", "sports", "tech"]


class ZSTopicClassification(Model):
    def __init__(self, candidate_labels=[]):
        self.classifier = pipeline("zero-shot-classification", model=model_id)
        self.candidate_labels = candidate_labels if len(
            candidate_labels) > 0 else default_candidate_labels

    def process(self, text, lang="en"):
        return self.classifier(text, self.candidate_labels, multi_label=False)

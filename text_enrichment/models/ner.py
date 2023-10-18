import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from models.base import Model

model_id = "Babelscape/wikineural-multilingual-ner"


class NERModel(Model):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForTokenClassification.from_pretrained(model_id)
        self.ner = pipeline("ner", model=model_id,
                            tokenizer=model_id, grouped_entities=True)

    def process(self, text, lang="en"):
        return self.ner(text)

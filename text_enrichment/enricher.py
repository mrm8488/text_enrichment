from models.ner import NERModel
from models.entity_linking import REBELLinkingModel
from models.zs_topic_classification import ZSTopicClassification

from utils.text_processor import TextProcessor
from utils.batch_handler import BatchHandler


class Enricher:
    MODEL_MAP = {
        "ner": NERModel,
        "entity_linking": REBELLinkingModel,
        "zs_topic": ZSTopicClassification
    }

    def __init__(self, models=[]):
        self.models = [self.MODEL_MAP[model]() for model in models]

    def process(self, text_input):
        processed_text = TextProcessor.prepare(text_input)
        batches = BatchHandler().batch_handler.handle(text=processed_text)

        enriched_data = {}
        for batch in batches:
            for model in self.models:
                result = model.process(batch)
                enriched_data.update(result)

        return enriched_data

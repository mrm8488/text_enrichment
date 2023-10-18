from abc import ABC, abstractmethod
import pysbd


# Define the Strategy Interface
class SplitStrategy(ABC):

    @abstractmethod
    def split(self, text):
        pass


# Implement Concrete Strategies
class CharacterStrategy(SplitStrategy):
    def split(self, text, char_limit=512):
        """Split the text by characters."""
        return [text[i:i+char_limit] for i in range(0, len(text), char_limit)]


class SentenceStrategy(SplitStrategy):
    def split(self, text):
        """Split the text by sentences."""
        seg = pysbd.Segmenter(language="en", clean=False)
        return seg.segment(text)


class ParagraphStrategy(SplitStrategy):
    def split(self, text):
        """Split the text by paragraphs."""
        return [p for p in text.split('\n') if p]


class DefaultStrategy(SplitStrategy):
    def split(self, text):
        return [text]

# Implement the BatchHandler using the Strategy Pattern


class BatchHandler:
    def __init__(self, strategy: SplitStrategy = DefaultStrategy()):
        self.strategy = strategy

    def handle(self, text):
        return self.strategy.split(text)

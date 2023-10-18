import torch
from transformers import pipeline
from models.base import Model

model_id = "'Babelscape/mrebel-bas"


class REBELLinkingModel(Model):
    def __init__(self):
        self.triplet_extractor = pipeline('translation_xx_to_yy',
                                          model=model_id, tokenizer=model_id)

    def _extract_triplets_typed(text):
        triplets = []
        relation = ''
        text = text.strip()
        current = 'x'
        subject, relation, object_, object_type, subject_type = '', '', '', '', ''

        for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").replace("tp_XX", "").replace("__en__", "").split():
            if token == "<triplet>" or token == "<relation>":
                current = 't'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(
                    ), 'tail': object_.strip(), 'tail_type': object_type})
                    relation = ''
                subject = ''
            elif token.startswith("<") and token.endswith(">"):
                if current == 't' or current == 'o':
                    current = 's'
                    if relation != '':
                        triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(
                        ), 'tail': object_.strip(), 'tail_type': object_type})
                    object_ = ''
                    subject_type = token[1:-1]
                else:
                    current = 'o'
                    object_type = token[1:-1]
                    relation = ''
            else:
                if current == 't':
                    subject += ' ' + token
                elif current == 's':
                    object_ += ' ' + token
                elif current == 'o':
                    relation += ' ' + token
        if subject != '' and relation != '' and object_ != '' and object_type != '' and subject_type != '':
            triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(
            ), 'tail': object_.strip(), 'tail_type': object_type})
        return triplets

    def process(self, text, lang="en"):
        extracted_text = self.triplet_extractor.tokenizer.batch_decode([self.triplet_extractor(text, src_lang=lang, return_tensors=True, return_text=False)[
            0]["translation_token_ids"]])  # change __en__ for the language of the source.
        print(extracted_text[0])
        extracted_triplets = self._extract_triplets_typed(extracted_text[0])
        print(extracted_triplets)
        return extracted_triplets

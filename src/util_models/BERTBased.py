from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch


class BERTBased:
    def __init__(self):
        model_path = "../../../models/bert-base-cased-squad2/saves"
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_path)

    def getAnswers(self, message, knowledge_source):
        print(f"Input: {message}")
        inputs = self.tokenizer.encode_plus(message, knowledge_source, return_tensors='pt')

        start_scores, end_scores = self.model(**inputs)

        token_start = torch.argmax(start_scores)
        token_end = torch.argmax(end_scores) + 1
        response = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][token_start:token_end]))
        print(f"Response: {response}")
        return response

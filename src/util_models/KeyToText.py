from transformers import AutoTokenizer, AutoModelWithLMHead
import torch as pt

class KeyToText:
    def __init__(self):
        self.tokenizer, self.model = self.load_tokenizer_and_model()

    def load_tokenizer_and_model(self, model_path="../../../models/keytotext-small/saves"):
        print ("Loading KeyToText")
        tokenizer = AutoTokenizer.from_pretrained("../../../models/bert-base-cased-squad2/saves")
        model = AutoModelWithLMHead.from_pretrained(model_path)
        return tokenizer, model

    def generate_sentence(self, keywords):
        pass
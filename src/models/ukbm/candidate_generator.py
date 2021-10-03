from ...util_models.BERTBase import BERTBase


class CandidateGenerator:
    def __init__(self, model_name, knowledge_source):
        if model_name == "BERTBased":
            self.model = BERTBase()
        else:
            raise Exception(f"Model {model_name} not recognized")
        self.knowledge_source = knowledge_source

    def getCandidateAnswers(self, message):
        return self.model.getAnswers(message, self.knowledge_source)

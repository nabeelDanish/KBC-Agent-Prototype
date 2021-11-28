from .candidate_generator import CandidateGenerator
from ...util_models.KeyToText import KeyToText

class ukbm:
    def __init__(self, knowledge_source):
        self.knowledge_source = knowledge_source
        self.candidateGenerator = CandidateGenerator("BERTBased", knowledge_source)
        # self.responseGenerator = KeyToText()

    def getResponse(self, message):
        return self.candidateGenerator.getCandidateAnswers(message)

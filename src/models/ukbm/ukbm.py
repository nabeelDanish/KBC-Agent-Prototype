from .candidate_generator import CandidateGenerator
from ...util_models.DialoGPT import DialoGPT


class ukbm:
    def __init__(self, knowledge_source):
        self.knowledge_source = knowledge_source
        self.candidateGenerator = CandidateGenerator("BERTBased", knowledge_source)
        self.chat_round = -1
        self.dialogueModel = DialoGPT()

    def getResponse(self, message):
        self.chat_round += 1
        return "Candidate Answer: " + self.candidateGenerator.getCandidateAnswers(message) \
               + " [BR] Dialogue Model response:" + self.dialogueModel.generate_response(self.chat_round, message)

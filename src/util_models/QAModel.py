from abc import ABC, abstractmethod


class QAModel:
    @abstractmethod
    def getAnswers(self, message, knowledge_source):
        pass

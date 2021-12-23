"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  APIModel Class
    - Provides the configuration settings to be used for the pipeline model
    - This allows the API Model to be highly configurable and interchangeable
"""

# Imports
from ...models.dykg.dykg import DYKG


# Class Definition
class APIModel:
    def __init__(self, source):
        self.params = {
            "source": source,
            "flavors": {
                "small": {
                    "dialoGPT": "../../../models/DialoGPT-small",
                    "t5": "../../../models/t5-small",
                    "bert": "../../../models/bert-base-cased-squad2",
                    "mpnet": "../../../models/all-mpnet-base-v2",
                    "t5-e2e": "../../../models/t5-small-e2e-qg",
                    "intent": "../../../models/intent.sav",
                },
                "medium": {
                    "dialoGPT": "../../../models/DialoGPT-medium",
                    "t5": "../../../models/t5-base",
                    "bert": "../../../models/bert-base-cased-squad2",
                    "mpnet": "../../../models/all-mpnet-base-v2",
                    "t5-e2e": "../../../models/t5-base-e2e-qg",
                    "intent": "../../../models/intent.sav",
                },
                "large": {
                    "dialoGPT": "../../../models/DialoGPT-medium",
                    "t5": "../../../models/t5-large",
                    "bert": "../../../models/bert-base-cased-squad2",
                    "mpnet": "../../../models/all-mpnet-base-v2",
                    "t5-e2e": "../../../models/t5-base-e2e-qg",
                    "intent": "../../../models/intent.sav",
                },
                "xlarge": {
                    "dialoGPT": "../../../models/DialoGPT-large",
                    "t5": "../../../models/t5-large",
                    "bert": "../../../models/bert-base-cased-squad2",
                    "mpnet": "../../../models/all-mpnet-base-v2",
                    "t5-e2e": "../../../models/t5-base-e2e-qg",
                    "intent": "../../../models/intent.sav",
                }
            },
            "selected_flavor": "large",
            "use_cuda": {
                "dialoGPT": True,
                "t5": True,
                "t5-e2e": False,
                "mpnet": True
            }
        }
        self.model = DYKG(self.params)

    def updateKnowledge(self, knowledge):
        self.model.set_knowledge_source(knowledge)

    def reply(self, message):
        return self.model.get_response(message)

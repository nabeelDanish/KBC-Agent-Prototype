"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  DYKG Class
    - Primary pipeline class for MUKALMA, as developed in Iteration 1 and 2 of the project
    - Defines a model that makes use of ann ensemble Knowledge-Retrieval module
    - In conjunction with a Language Model for dialog generation.
    - This model should be used for generating human-like dialog grounded on knowledge.
"""

# Importing Models
from ...util_models.DialoGPTController import DialoGPTController
from src.util_models.T5.T5ClozeController import T5ClozeController, getMaskToken
from ...util_models.MpNet import MpNet
from ...util_models.T5.T5ForQuestionGeneration import T5ForQuestionGeneration

# Importing NLU Components
from .nlu.partsOfSpeech import get_nouns, match_questions, match_nouns_from_set, truecasing_by_pos, fix_sentence
from .nlu.svo_utils import nlp
from .nlu.intentRecognition import IntentRecognizer

from torch import cuda


# Class Definition
class DYKG:
    def __init__(self, params):
        """
        function to initialize the model pipeline
        :param knowledge_source: a python str of raw text that contains the knowledge source on which the model attends
                                 over
        """
        self.TAG = 'DYKG'

        # Check for Nvidia CUDA Support on the machine
        cuda.empty_cache()
        print(f"{self.TAG}: CUDA GPU is {'not' if not cuda.is_available() else ''} available on this machine")

        # ---------- Setting up the Knowledge Source
        self.secondary_knowledge_dict = {}
        self.current_turn_knowledge = ""
        self.set_knowledge_source(params["source"])

        # Parameter Configurations
        self.flavor_selected = params["selected_flavor"]
        self.flavor_config = params["flavors"][self.flavor_selected]
        self.model_flavors = params["flavors"]
        self.cuda_use = params["use_cuda"]

        # ---------- Initialize all sub-models used by this model

        self.intentRecognizer = IntentRecognizer(model_path=self.flavor_config["intent"])

        self.dialogue_model = DialoGPTController(self.flavor_config["dialoGPT"], use_cuda=self.cuda_use["dialoGPT"])
        self.dialogue_model.initialize_model(refresh=True)

        self.sentence_model = MpNet(self.flavor_config["mpnet"], use_cuda=self.cuda_use["mpnet"])

        self.question_generation_model = T5ForQuestionGeneration(self.flavor_config["t5-e2e"], use_cuda=self.cuda_use["t5-e2e"])
        self.question_generation_model.initialize_model()

        self.cloze_model = T5ClozeController(self.flavor_config["t5"], use_cuda=self.cuda_use["t5"], num_responses=3)
        self.cloze_model.initialize_model()

        # Initializing Total nouns and verbs in the text
        self.knowledge_source_pos = set()
    # End of function

    def load_knowledge_source_pos(self, knowledge_source):
        self.knowledge_source_pos = set(get_nouns(knowledge_source))

    def set_knowledge_source(self, knowledge_source):
        self.knowledge_source = knowledge_source
        self.sent_tok_knowledge = [sent.text for sent in nlp(knowledge_source).sents]

        # Loading POS entities
        self.load_knowledge_source_pos(knowledge_source)

    def __set_combined_knowledge_source_for_turn(self):
        # self.knowledge_model.setKnowledgeSource(self.current_turn_knowledge)
        self.sent_tok_knowledge = [sent.text for sent in nlp(self.current_turn_knowledge).sents]

        # Loading POS entities
        if len(self.current_turn_knowledge) != 0:
            self.load_knowledge_source_pos(self.current_turn_knowledge)

    def fetch_secondary_knowledge(self, message):
        # Reset the combined knowledge source for this turn
        self.current_turn_knowledge = ""

        # Uncomment the below code to allow for Wikipedia looking up during the conversation
        # This allows the conversation agent to move from one topic to another
        """
        # Extract the named entities from the message sent by the user
        # Attempt to find a wikipedia article corresponding to each named entity and extract a summary
        # Append these summaries to the knowledge source in order to make the information available to our model
        named_entities = extract_named_entities(message, get_non_numeric_named_entities())
        for named_entity in named_entities:
            print(f"[{self.TAG}]: [fetch_secondary_knowledge]: Fetching knowledge for {named_entity}")
            if named_entity not in self.secondary_knowledge_dict:
                topic_summary = getTopicSummary(named_entity)
                if topic_summary is not None:
                    self.secondary_knowledge_dict[named_entity] = topic_summary
                    self.current_turn_knowledge += topic_summary
                else:
                    print(f"[{self.TAG}]: [fetch_secondary_knowledge]: Could not find knowledge for {named_entity}")
            else:
                self.current_turn_knowledge += self.secondary_knowledge_dict[named_entity]

        # Append the primary knowledge to the end
        # If any named entities were found, they should be more relevant than the primary knowledge and should be closer
        # to the beginning of the text
        # self.current_turn_knowledge += self.knowledge_source
        """

        # FOR DEBUGGING PURPOSES START
        # Comment this line if you don't want to change topic: by Nabeel Danish
        self.current_turn_knowledge = self.knowledge_source
        # FOR DEBUGGING PURPOSES END

        print(f"[{self.TAG}]: {self.current_turn_knowledge}\n")

    # End of function

    def get_best_response_id(self, responses, log_responses=False, prefix=""):
        max_length = -1
        max_id = 0
        for response_id, response in enumerate(responses):
            if log_responses:
                print(f"[{self.TAG}: {prefix} {response_id}]: {response} .")
            if len(response) > max_length:
                max_length = len(response)
                max_id = response_id

        return max_id
    # End of function

    def generate_knowledge_based_response(self, message, knowledge_sent, extracted_question):
        message = fix_sentence(message)

        # If a relevant knowledge sentence couldn't be found, return the best response the dialogue model could generate
        if knowledge_sent == "":
            responses = self.dialogue_model.predict(message, output_fragment=knowledge_sent)
            return responses[self.get_best_response_id(responses)], responses

        # Take the word / phrase retrieved from the knowledge source and complete it
        # This is done by framing this task as a Cloze task
        cloze_responses = self.cloze_model.generate_cloze_responses(
            f"{message} {getMaskToken(0)} {knowledge_sent} {getMaskToken(1)} .".lower()
        )

        fragmented_outputs = []
        outputs = []
        for cloze_response in cloze_responses:
            # Take the the output with the 'blanks' filled. Take a slice of the output by removing the input prompt
            # from it. Use a dialogue model to complete this output slice, in an attempt to make the reply open ended
            knowledge_sent = cloze_response[len(message) + 1:-2] + "."

            # We use two methods to generate the output. One sentence is a knowledge-grounded response. The second,
            # following sentence is a dialog-style response which follows from the first generated sentence
            # We need to keep track of this separation between the two sentences
            fragmented_output = [(knowledge_sent, dialog)
                                 for dialog in self.dialogue_model.predict(message, output_fragment=knowledge_sent)]
            output = [kg + dg for (kg, dg) in fragmented_output]

            fragmented_outputs.extend(fragmented_output)
            outputs.extend(output)

            print(f"OUTPUTS: \n{fragmented_output}")

        # Obtain the index of the best response, and lookup the best response string (complete and fragmented on the
        # basis of the method used to generate the string)
        best_response_id = self.get_best_response_id(outputs)
        best_fragmented_response = fragmented_outputs[best_response_id]
        best_response = outputs[best_response_id]

        # Check if the answer generated by the dialog model 'follows from' the generated knowledge-grounded output
        # at index 0 of the fragmented response
        self.cloze_model.check_equivalence(
            best_fragmented_response[1], f"{self.knowledge_source}. {extracted_question} {best_fragmented_response[0]}"
        )

        # Swap the best response to index 0 to indicate that this was the selected response
        outputs[best_response_id] = outputs[0]
        outputs[0] = best_response

        return best_response, outputs
    # End of function

    def find_relevant_response(self, message):
        selected_question = message

        # Matching Nouns
        if match_nouns_from_set(message, self.knowledge_source_pos) == 0:
            return selected_question, "", -1, -1

        # Intent Recognition
        intent = self.intentRecognizer.recognizeIntent(message)
        print(f"[{self.TAG}]: Intent: {intent}")
        knowledge_sent, knowledge_start_index, knowledge_end_index = "", -1, -1

        # Setting the question from the either the message (if the message was a question)
        # Or generate a question from the statement
        if intent == "Statement":
            knowledge_questions = self.question_generation_model.generate_questions(message, "")
            knowledge_question = knowledge_questions[0] if len(knowledge_questions) > 0 else None
        else:
            knowledge_question = message

        # Fetching answer from T5
        if knowledge_question is not None:
            print(f"[{self.TAG}]: [Message-Question]: {knowledge_question}")
            selected_question = knowledge_question
            knowledge_sent, knowledge_start_index, knowledge_end_index = \
                self.cloze_model.get_answers(message, self.current_turn_knowledge)
            print(f"[{self.TAG}]: [CLOZE-Based]: Knowledge sent: {knowledge_sent}")

        # If a knowledge_sent couldn't be found, find the most similar sentence instead
        if len(knowledge_sent) == 0:
            print(f"[{self.TAG}]: SENT TOK KNOWLEDGE: { self.sent_tok_knowledge }")
            print(f"\n\nSENT TOK KNOWLEDGE:\n{self.sent_tok_knowledge[:4]}\n\nmessage:\n{message}")
            knowledge_sent, knowledge_start_index, knowledge_end_index = \
                self.sentence_model.get_most_similar_sentence(message, self.sent_tok_knowledge), -1, -1

            if len(knowledge_sent) != 0:
                # Generate a question from the message and the similar sentence
                knowledge_questions = []
                message_nouns = get_nouns(message)

                print(f"[{self.TAG}]: Using the message nouns: {message_nouns}")

                # Finding all the questions for each noun we identify in the message
                message_keyword = " ".join(message_nouns)
                knowledge_questions.extend(self.question_generation_model.generate_questions(knowledge_sent, message_keyword))
                print(f"[{self.TAG}]: Questions Generated: {knowledge_questions}")

                # Select the most relevant question from the list of generated questions
                # based on basic word matching
                selected_questions = match_questions(message, knowledge_questions, knowledge_sent)

                # Obtain the knowledge span by querying the source using a QA model and the best question
                if len(selected_questions) != 0:
                    selected_question = selected_questions[0]
                    print(f"[{self.TAG}]: Using the question: {selected_question}")

                    knowledge_sent, knowledge_start_index, knowledge_end_index = \
                        self.cloze_model.get_answers(selected_question, knowledge_sent)
                else:
                    knowledge_sent, knowledge_start_index, knowledge_end_index = "", -1, -1
                    selected_question = message
                # End else
            else:
                selected_question = message
            # End if
        # End if

        # Logging and Return
        print(f"[{self.TAG}]: Response: {knowledge_sent} start span: {knowledge_start_index} end span: {knowledge_end_index}")
        return selected_question, knowledge_sent, knowledge_start_index, knowledge_end_index

    def get_response(self, message):
        self.fetch_secondary_knowledge(message)
        self.__set_combined_knowledge_source_for_turn()

        # Retrieve the relevant knowledge sentence from the knowledge source
        selected_question, knowledge_sent, knowledge_start_index, knowledge_end_index = self.find_relevant_response(
            message)

        # Condition on the knowledge sentence, and generate knowledge-grounded dialog
        best_response, knowledge_grounded_responses = \
            self.generate_knowledge_based_response(message, knowledge_sent, selected_question)

        # Cleaning the responses
        best_response = truecasing_by_pos(best_response)
        for i in range(len(knowledge_grounded_responses)):
            knowledge_grounded_responses[i] = truecasing_by_pos(knowledge_grounded_responses[i])

        # Logging and Return
        print(f"[{self.TAG}]: GENERATED RESPONSE: { knowledge_grounded_responses }")
        return { "knowledge_sent": knowledge_sent,
                 "response": best_response, "candidates": knowledge_grounded_responses,
                "k_start_index": knowledge_start_index, "k_end_index": knowledge_end_index }
    # End of function
# End of class

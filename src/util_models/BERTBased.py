"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  BERTBased class - responsible for initializing a BERT model, or a similar model like ALBERT, RoBERTa.
    Provides methods for:
    - Question Answering: Given a knowledge source and question, it picks out an answer span
    - Calculating Sentence Similarity scores based on embeddings in the hidden layer

  @Date: 17th October, 2021
"""

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import numpy as np
from scipy import spatial
from torch import cuda
from rich.console import Console

console = Console(record=True)


class BERTBased:
    def __init__(self, model_path='../../../models/bert-base-cased-squad2', use_cuda=False):
        self.TAG = 'BERTBased'

        self.model_path = model_path

        self.device = 'cuda' if use_cuda and cuda.is_available() else 'cpu'
        cuda.empty_cache()

        self.tokenizer = self.model = None
        self.initialize_model()

    def initialize_model(self, refresh=False):
        # Loads model from disk into memory
        if self.tokenizer is None or refresh:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)

        if self.model is None or refresh:
            console.log(f"""[{self.TAG}]: Loading {self.model_path}...\n""")
            self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_path, local_files_only=True)\
                .to(self.device)

    def get_answers(self, message, knowledge_source):
        print(f"Input: {message}\nKnowledge Source: {knowledge_source[0:30]}")

        # Encode the inputs
        inputs = self.tokenizer.encode_plus(message, knowledge_source, return_tensors='pt').to(self.device)

        # Feed them to the model to obtain two output projections
        # One is a probability distribution over the possible start position of the answer span, the other is a
        # distribution over the possible end positions.
        start_scores, end_scores = self.model(**inputs, return_dict=False)

        # Use the tokenizer in reverse to obtain the response span, if the start position occurs after the end position,
        # then that means that the model could not find a reponse span, and believes that the answer is not present
        # in the knowledge source. In this case, the response string will be [CLS]
        token_start = torch.argmax(start_scores)
        token_end = torch.argmax(end_scores) + 1
        response = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][token_start:token_end]))

        # Attempt to obtain the offset for the start of the span
        # TODO: Not working correctly if the knowledge source contains indented text
        answer_prefix = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][:token_start], skip_special_tokens=True)
        )
        span_start_index = len(answer_prefix) - len(message)
        span_end_index = span_start_index + len(response)

        print(f"[{self.TAG}] Response: {response}\nanswer prefix: {answer_prefix}\n\n, start index: {span_start_index},"
              f" end index: {span_end_index}")
        return response if response != "[CLS]" else "", span_start_index, span_end_index

    def vectorize(self, sentences):
        tokenized = list(map(lambda x: self.tokenizer.encode(x, add_special_tokens=True), sentences))

        # Find the maximum length sequence so it can be used for padding the other tokenized outputs
        max_len = 0
        for i in tokenized:
            if len(i) > max_len:
                max_len = len(i)

        # Pad the other sequences
        padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized])
        input_ids = torch.tensor(np.array(padded)).type(torch.LongTensor).to(self.device)
        # attention_mask = torch.tensor(np.where(padded != 0, 1, 0)).type(torch.LongTensor)

        # Feed the batch of inputs to the model and extract hidden_states
        with torch.no_grad():
            last_hidden_states = self.model(input_ids, output_hidden_states=True).hidden_states

        print(f"hidden state type: {type(last_hidden_states)}")
        # print(f"hidden state shape: {np.array(list(last_hidden_states)).shape}")
        vectors = np.array(last_hidden_states[11][:, 11, :])
        print(f"Vectors length: {vectors.shape}")
        return vectors

    def get_most_similar_sentence(self, sentence, candidates):
        """
        Given the sentence to be matched, find the candidate sentence that is most similar using BERT's hidden states
        :param sentence: Sentence to be matched
        :param candidates: Candidates from which the one that is most similar to sentence must be found
        :return: The candidate sentence that is most similar to the sentence parameter
        """
        sentences = [sentence]
        sentences.extend(candidates)

        # Vectorize sentence to be matched, and all candidate sentences in a batch
        vectorized_sentences = self.vectorize(sentences)
        sent_vector = vectorized_sentences[0]
        candidate_vectors = vectorized_sentences[1:]

        # Find the candidate sentence that is most similar to the sentence to be matched
        max_distance = -1
        most_similar_sentence = None
        for candidate_id, candidate_vector in enumerate(candidate_vectors):
            # print(f"sent vector:\n{sent_vector}\n\ncandidate vec:\n{candidate_vector}")
            distance = spatial.distance.cosine(sent_vector, candidate_vector)
            print(f"sentence: {candidates[candidate_id]}\tscore: {distance}")
            if distance > max_distance:
                max_distance = distance
                most_similar_sentence = candidates[candidate_id]

        return most_similar_sentence

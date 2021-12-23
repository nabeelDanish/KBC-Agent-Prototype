"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  T5ClozeController - Module that acts as a controller for a T5 Model
  - Applies the T5 model on a Cloze (fill-in-the-blanks) task.
  - Masked LM was used as one of the T5 Model's pre-training tasks, hence, it is particularly suited to being applied on
    Cloze tasks.
  - Sentinel tokens are effectively mask tokens used by the T5 tokenizer to represent blanks that must be
    filled.

  @Author: Muhammad Farjad Ilyas
  @Date: 6th December, 2021
"""

import torch
from rich.console import Console

# Import T5's modules from huggingface's transformers
from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration

console = Console()


def getMaskToken(mask_id):
    return "<extra_id_" + str(mask_id) + ">"


class T5ClozeController:
    def __init__(self, model_path, num_responses=3, use_cuda=False):
        self.TAG = 'T5ClozeController'

        self.device = 'cuda' if use_cuda and torch.cuda.is_available() else 'cpu'
        torch.cuda.empty_cache()

        self.model_path = model_path

        # Initial values for model and tokenizer
        self.model = None
        self.tokenizer = None

        self.num_responses = num_responses

    def initialize_model(self, refresh=False):
        # Load model from disk into memory
        if self.tokenizer is None or refresh:
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
        if self.model is None or refresh:
            console.log(f"""[{self.TAG}]: Loading {self.model_path}...\n""")
            print(f"{self.TAG}: CUDA IS {'NOT' if not torch.cuda.is_available() else ''} AVAILABLE")

            model_config = T5Config.from_pretrained(self.model_path, local_files_only=True)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_path, config=model_config,
                                                                    local_files_only=True)
            self.model = self.model.to(self.device)

    def fill_masks(self, text, output):
        result = ""

        starting_mask = "<extra_id_0>"
        if starting_mask in text:
            result = text[:text.index(starting_mask)]
        else:
            return text

        _txt = self.tokenizer.decode(output, skip_special_tokens=False, clean_up_tokenization_spaces=False)

        for i in range(0, 100):
            cur_mask = "<extra_id_" + str(i) + ">"
            next_mask = "<extra_id_" + str(i + 1) + ">"

            # Calculate the text to fill the mask
            # If the model was not able to fill the current blank, then replace the mask with an empty string
            # print(f"Decoded text: {_txt}")
            if cur_mask in _txt:
                _prev_end_token_index = _txt.index(cur_mask) + len(cur_mask)
                if next_mask in _txt:
                    _end_token_index = _txt.index(next_mask)
                else:
                    _end_token_index = len(_txt)
                # print(f"Text to fill mask: {_txt[_prev_end_token_index:_end_token_index]}")

                # Fill the current mask
                mask_fill_text = _txt[_prev_end_token_index:_end_token_index]

                if all([x.isalpha() or x == ' ' for x in mask_fill_text]):
                    result = result + mask_fill_text

            # get the index right after the mask being replaced
            suffix_start_index = text.index(cur_mask) + len(cur_mask)

            if next_mask in text:
                # There is a mask which hasn't been filled, append the string up till that mask
                # The mask that has been found will be filled in the next loop
                suffix_end_index = text.index(next_mask)
            else:
                # All the masks present in the original text have been replaced
                # Append any remaining text after the last replaced mask and return the filled string
                return result + text[suffix_start_index:]

            # Append the result string with the substring after the mask that was filled in this loop
            # Up till the next mask, of the end of the string, whichever comes first
            result = result + text[suffix_start_index:suffix_end_index]

    def generate_cloze_responses(self, text):
        encoded = self.tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')
        input_ids = encoded['input_ids'].to(self.device)

        print(f"INPUT TEXT: {text}")

        # Generating 20 sequences with maximum length set to 5
        outputs = self.model.generate(input_ids=input_ids, num_beams=200,
                                      num_return_sequences=self.num_responses, max_length=5)

        results = []
        for output in outputs:
            result = self.fill_masks(text, output)
            print(f"Result: {result}")
            results.append(result)

        return results

    def check_equivalence(self, hypothesis, premise):
        print(f"[{self.TAG}]: [check_equivalence]:\n[hypothesis]: {hypothesis}\npremise: {premise}\n")
        inp = f"mnli hypothesis: {hypothesis}. premise: {premise}"

        input_ids = self.tokenizer(inp, return_tensors='pt', add_special_tokens=True).input_ids.to(self.device)
        outputs = self.model.generate(input_ids)

        for output in outputs:
            print(f"[{self.TAG}]: [check_equivalence]: {self.tokenizer.decode(output, skip_special_tokens=True)}")

    def get_answers(self, message, knowledge_source):
        question = f"question: {message} context: {knowledge_source}"
        input_ids = self.tokenizer(question, return_tensors='pt', add_special_tokens=True).input_ids.to(self.device)
        outputs = self.model.generate(input_ids)

        decoded_outputs = []
        for output in outputs:
            decoded_output = self.tokenizer.decode(output, skip_special_tokens=True)
            print(f"[{self.TAG}]: [get_answers: QA]: {decoded_output}")
            decoded_outputs.append(decoded_output)

        # decoded_outputs[0] = "Mumbai"
        inp = f"mnli hypothesis: {decoded_outputs[0]} . premise: {knowledge_source} {message}"

        input_ids = self.tokenizer(inp, return_tensors='pt', add_special_tokens=True).input_ids.to(self.device)
        eq_outputs = self.model.generate(input_ids)
        eq_checks = []

        for eq_output in eq_outputs:
            eq_check = self.tokenizer.decode(eq_output, skip_special_tokens=True)
            eq_checks.append(eq_check)
            print(f"[{self.TAG}]: [get_answers: sanity_check]: {eq_check}")

        return decoded_outputs[0] if eq_checks[0] == 'entailment' else "", -1, -1

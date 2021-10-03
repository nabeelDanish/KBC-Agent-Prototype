from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class DialoGPT:
    def __init__(self):
        self.tokenizer, self.model = self.load_tokenizer_and_model()
        self.chat_history_ids = None

    def load_tokenizer_and_model(self, model="../../../models/DialoGPT-small//saves"):
        """
          Load tokenizer and model instance for some specific DialoGPT model.
        """
        # Initialize tokenizer and model
        print("Loading DialoGPT model...")
        tokenizer = AutoTokenizer.from_pretrained(model)
        model = AutoModelForCausalLM.from_pretrained(model)

        # Return tokenizer and model
        return tokenizer, model

    def generate_response(self, chat_round, message):
        """
          Generate a response to some user input.
        """
        # Encode user input and End-of-String (EOS) token
        new_input_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors='pt')

        # Append tokens to chat history
        bot_input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1) if chat_round > 0 else new_input_ids

        # Generate response given maximum chat length history of 1250 tokens
        self.chat_history_ids = self.model.generate(bot_input_ids, max_length=1250,
                                                    pad_token_id=self.tokenizer.eos_token_id)

        return self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

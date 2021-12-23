"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  T5ForQuestionGeneration - Module that acts as a controller for a T5 Model
  - Applies the T5 model on a Question Generation task.

  @Author: Muhammad Farjad Ilyas
  @Date: 9th December, 2021
"""


import torch
from rich.console import Console
from ..T5.pipelines import pipeline

console = Console()


class T5ForQuestionGeneration:
    def __init__(self, model_path='../../../models/t5-base-e2e-qg', use_cuda=False):
        self.TAG = 'T5ForQuestionGeneration'

        self.model_path = model_path
        self.use_cuda = use_cuda

        # Initial values for model
        self.model = None

    def initialize_model(self, refresh=False):
        if self.model is None or refresh:
            console.log(f"""[{self.TAG}]: Loading {self.model_path}...\n""")
            self.model = pipeline("e2e-qg", model=self.model_path, use_cuda=self.use_cuda)

    def generate_questions(self, source_text, context):
        return self.model(f"{source_text} {context}")

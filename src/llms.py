import os

from langchain_community.llms import Ollama, OpenAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class LLMs:
    def __init__(self):
        self.openai_gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
        self.openai_gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.1)
        self.llama3 = Ollama(model="llama3", temperature=0.1)
        self.ollama_hermes = Ollama(model="openhermes", temperature=0.1)
        self.ollama_mistral = Ollama(model="mistral", temperature=0.1)
        self.ollama_mixtral = Ollama(model="mixtral", temperature=0.1)
        self.claude = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")

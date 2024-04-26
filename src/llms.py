import os
from dotenv import load_dotenv

from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class LLMs:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        is_local = os.getenv("IS_LOCAL", "false").lower() == "true"
        if is_local:
            self.llm_map = {
                "Claude3 Opus": ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229"),
                "GPT-35. Turbo": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1),
                "GPT-4": ChatOpenAI(model_name="gpt-4", temperature=0.1),
                "llama3": Ollama(model="llama3", temperature=0.1),
                "openhermes": Ollama(model="openhermes", temperature=0.1),
                "mistral": Ollama(model="mistral", temperature=0.1),
                "mixtral": Ollama(model="mixtral", temperature=0.1)
            }
        else:
            self.llm_map = {
                "Claude3 Opus": ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229"),
                "GPT-35. Turbo": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1),
                "GPT-4": ChatOpenAI(model_name="gpt-4", temperature=0.1)
            }

    def get_llm(self, llm_name):
        return self.llm_map.get(llm_name)

    def get_available_llms(self):
        return list(self.llm_map.keys())
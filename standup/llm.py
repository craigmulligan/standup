from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain_community.llms import GPT4All
from langchain_community.llms import Ollama
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class BaseLLM:
    """
    Base class for LLM instances with common functionality.
    """

    def __init__(self, config):
        self.config = config
        self.llm = self._create_model()

    def _create_model(self):
        """
        Factory method pattern implemented in subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def summarize_docs(self, docs, prompt):
        summarize_chain = load_summarize_chain(self.llm, prompt=prompt)
        return summarize_chain.invoke(docs)

    def text_splitter(self, text):
        texts = RecursiveCharacterTextSplitter(chunk_size=int(self.config.get("chunk_size")),
                                               chunk_overlap=int(self.config.get("chunk_overlap"))
                                               ).split_text(text)
        docs = [Document(page_content=t) for t in texts]
        return docs


class LocalLLM(BaseLLM):
    """
    LLM that works locally on the user's machine.
    """

    def _create_model(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = GPT4All(
            model=self.config["model_path"],
            n_ctx=int(self.config["max_tokens"]),
            callback_manager=callback_manager
        )
        return llm


class OpenAILLM(BaseLLM):
    """
    LLM that sends queries to OpenAI's API.
    """

    def _create_model(self):
        return ChatOpenAI(
            model=self.config["model_name"],
            api_key=self.config["api_key"],
            max_tokens=int(self.config["max_tokens"])
        )


class OLLamaLLM(BaseLLM):
    """
    LLM that works locally on the user's machine.
    """

    def _create_model(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = Ollama( 
            model=self.config["model_name"],
            base_url=self.config["base_url"],
            callback_manager=callback_manager
        )
        return llm

def llm_factory(config):
    """
    Factory function to create an LLM instance based on config.
    """
    if config["model_type"] == "openai":
        return OpenAILLM(config)
    elif config["model_type"] == "ollama":
        return OLLamaLLM(config)
    else:
        return LocalLLM(config)

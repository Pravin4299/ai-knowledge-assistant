from langchain_ollama import ChatOllama

from app.core.config import settings


class LLMService:

    _llm = ChatOllama(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.3
    )

    @classmethod
    def generate_response(
        cls,
        messages
    ):

        response = cls._llm.invoke(messages)

        return response.content

    @classmethod
    def generate_text(
        cls,
        prompt: str
    ):

        response = cls._llm.invoke(prompt)

        return response.content
    
    @classmethod
    def stream_response(cls, messages):
        for chunk in cls._llm.stream(messages):
            if chunk.content:
                yield chunk.content
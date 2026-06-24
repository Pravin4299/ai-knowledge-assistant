from app.services.llm_service import LLMService


class QueryRewriteService:

    @staticmethod
    def rewrite(
        history_text: str,
        question: str
    ):

        prompt = f"""
You are a search query optimizer.

Rewrite the user's latest question
into a fully standalone question.

Rules:

1. Preserve meaning.
2. Expand references such as:
   it, they, that, those.
3. Use conversation context.
4. Return ONLY the rewritten question.

Conversation:
{history_text}

Question:
{question}

Standalone Question:
"""

        return (
            LLMService.generate_text(
                prompt
            )
            .strip()
        )
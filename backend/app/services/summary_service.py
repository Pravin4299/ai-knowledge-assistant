from app.repositories.message_repository import MessageRepository
from app.services.llm_service import LLMService


class SummaryService:

    @staticmethod
    def generate_summary(
        db,
        session
    ):

        messages = MessageRepository.get_session_messages(
            db=db,
            session_id=session.id
        )

        if len(messages) < 20:
            return

        conversation_text = "\n".join(
            [
                f"{msg.role}: {msg.content}"
                for msg in messages[-20:]
            ]
        )

        prompt = f"""
Summarize this conversation in under 300 words.

{conversation_text}
"""

        summary = LLMService.generate_text(
            prompt
        )

        session.conversation_summary = summary

        db.commit()
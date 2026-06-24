from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.message_service import MessageService
from app.core.config import settings
from app.services.summary_service import SummaryService
class StreamChatService:

    @staticmethod
    def stream_chat(
        db,
        session,
        question: str
    ):

        MessageService.create_user_message(
        db=db,
            session=session,
            content=question
        )

        history = MessageRepository.get_recent_messages(
            db=db,
            session_id=session.id,
            limit=settings.MAX_CHAT_HISTORY
        )

        messages = ConversationService.build_messages(
            history=history,
            question=question,
            summary=session.conversation_summary
        )



        answer = LLMService.generate_response(
            messages
        )

        full_response = ""

        for chunk in LLMService.stream_response(messages):
            full_response += chunk
            yield chunk


        MessageService.create_assistant_message(
            db=db,
            session=session,
            content=full_response
        )

        # Generate/update summary every 20 messages
        if session.message_count > 0 and session.message_count % 20 == 0:
            SummaryService.generate_summary(
                db=db,
                session=session
            )

        #return answer

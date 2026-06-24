from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.message_service import MessageService
from app.core.config import settings
from app.services.summary_service import SummaryService
from app.services.title_service import TitleService
import json
class AIChatService:

    @staticmethod
    def chat(
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

        MessageService.create_assistant_message(
            db=db,
            session=session,
            content=answer
        )


        print("session.title==========",session.title)
        if session.title == "New Chat":

            TitleService.generate_title(
                db=db,
                session=session,
                question=question
            )

        # Generate/update summary every 20 messages
        if session.message_count > 0 and session.message_count % 20 == 0:
            SummaryService.generate_summary(
                db=db,
                session=session
            )

        return answer
    
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
        print("messages======",messages)
        def generate():

            full_answer = ""

            for token in LLMService.stream_response(
                messages
            ):

                full_answer += token

                #yield f"data: {token}\n\n"
                yield (
                    f"data: {json.dumps({'token': token})}\n\n"
                )

            MessageService.create_assistant_message(
                db=db,
                session=session,
                content=full_answer
            )

            print("session.title==========",session.title)
            if session.title == "New Chat":

                TitleService.generate_title(
                    db=db,
                    session=session,
                    question=question
                )

            if (
                session.message_count > 0
                and
                session.message_count % 20 == 0
            ):
                SummaryService.generate_summary(
                    db=db,
                    session=session
                )

            #yield 'data: {"done": true}\n\n'
            yield (
                "data: "
                + json.dumps({
                    "done": True,
                    "sources": []
                })
                + "\n\n"
            )

        return generate()

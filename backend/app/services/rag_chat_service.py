from app.repositories.message_repository import MessageRepository

from app.services.llm_service import LLMService
from app.services.message_service import MessageService
from app.services.retrieval_service import RetrievalService
from app.services.rag_conversation_service import (
    RAGConversationService
)

from app.services.hybrid_retrieval_service import(
    HybridRetrievalService
)
from app.services.conversation_context_service import (ConversationContextService)
from app.services.query_rewrite_service import (QueryRewriteService)
from app.services.summary_service import (SummaryService)
from app.services.citation_service import (
    CitationService
)
from app.services.title_service import TitleService
from app.core.config import settings
import json

class RAGChatService:

    @staticmethod
    def chat(
        db,
        session,
        question: str,
        user_id: str
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

        history_text = (
            ConversationContextService
            .build_history_text(
                history
            )
        )

        if len(history) <= 1:
            standalone_question = question
        else:
            standalone_question = (
                QueryRewriteService.rewrite(
                    history_text=history_text,
                    question=question
                )
            )

        
        if not standalone_question:
            standalone_question = question
        
        print(
            "Original:",
            question
        )

        print(
            "Rewritten:",
            standalone_question
        )
        chunks = HybridRetrievalService.retrieve(
            db=db,
            user_id=user_id,
            question=standalone_question,
            top_k=3
        )

        # context = "\n\n".join(
        #     [
        #         chunk["chunk_text"]
        #         for chunk in chunks
        #     ]
        # )

        context_parts = []

        for chunk in chunks:

            context_parts.append(
                f"""
        SOURCE:
        {chunk["filename"]}

        CHUNK:
        {chunk["chunk_index"]}

        CONTENT:
        {chunk["chunk_text"]}
        """
            )

        context = "\n\n".join(
            context_parts
        )

        sources = (
            CitationService.build_sources(
                chunks
            )
        )
        messages = (
            RAGConversationService.build_messages(
                history=history,
                context=context,
                question=question
            )
        )

        answer = (
            LLMService.generate_response(
                messages
            )
        )
        print("chunks=========",chunks)
        if not chunks:

            answer = (
                "I could not find that "
                "information in the uploaded documents."
            )

        MessageService.create_assistant_message(
            db=db,
            session=session,
            content=answer
        )

        # Generate/update summary every 20 messages
        if session.message_count > 0 and session.message_count % 20 == 0:
            SummaryService.generate_summary(
                db=db,
                session=session
            )
        # return {
        #     "answer": answer,
        #     "sources": [
        #         {
        #             "chunk_index": chunk["chunk_index"],
        #             "distance": chunk["distance"]
        #         }
        #         for chunk in chunks
        #     ]
        # }

        return {
            "answer": answer,
            "sources": sources
        }
    
    @staticmethod
    def stream_chat(
        db,
        session,
        question: str,
        user_id: str
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

        history_text = (
            ConversationContextService
            .build_history_text(
                history
            )
        )

        if len(history) <= 1:
            standalone_question = question
        else:
            standalone_question = (
                QueryRewriteService.rewrite(
                    history_text=history_text,
                    question=question
                )
            )

        if not standalone_question:
            standalone_question = question

        print("Original:", question)
        print("Rewritten:", standalone_question)

        chunks = HybridRetrievalService.retrieve(
            db=db,
            user_id=user_id,
            question=standalone_question,
            top_k=3
        )

        print("chunks=========", chunks)

        sources = (
            CitationService.build_sources(
                chunks
            )
        )

        if not chunks:

            answer = (
                "I could not find that "
                "information in the uploaded documents."
            )

            MessageService.create_assistant_message(
                db=db,
                session=session,
                content=answer
            )

            def no_result_generator():

                yield (
                    f"data: {answer}\n\n"
                )

                yield (
                    f"data: "
                    f'{{"done": true}}'
                    f"\n\n"
                )

            return no_result_generator()

        context_parts = []

        for chunk in chunks:

            context_parts.append(
                f"""
    SOURCE:
    {chunk["filename"]}

    CHUNK:
    {chunk["chunk_index"]}

    CONTENT:
    {chunk["chunk_text"]}
    """
            )

        context = "\n\n".join(
            context_parts
        )

        messages = (
            RAGConversationService.build_messages(
                history=history,
                context=context,
                question=question
            )
        )

        def generate():

            full_answer = ""

            for token in LLMService.stream_response(
                messages
            ):

                full_answer += token

                # yield (
                #     f"data: {token}\n\n"
                # )
                yield (
                    f"data: {json.dumps({'token': token})}\n\n"
                )
            MessageService.create_assistant_message(
                db=db,
                session=session,
                content=full_answer
            )

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

            

            yield (
                "data: "
                + json.dumps({
                    "done": True,
                    "sources": sources
                })
                + "\n\n"
            )
            # yield (
            #     f"data: "
            #     f'{{"done": true, "sources": {sources}}}'
            #     f"\n\n"
            # )

        return generate()
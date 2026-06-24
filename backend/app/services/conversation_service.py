from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage


class ConversationService:

    @staticmethod
    def build_messages(
        history,
        question: str,
        summary: None
    ):

        system_content = (
            "You are a helpful AI assistant."
            "Answer clearly and accurately."
        )

        if summary:
            system_content += (
                f"\nConversation Summary:\n{summary}"
            )

        messages = [
            SystemMessage(
                content=system_content
            )
        ]

        #history = list(reversed(history))

        for msg in history:

            if msg.role == "user":
                messages.append(
                    HumanMessage(
                        content=msg.content
                    )
                )

            elif msg.role == "assistant":
                messages.append(
                    AIMessage(
                        content=msg.content
                    )
                )

        messages.append(
            HumanMessage(
                content=question
            )
        )

        return messages
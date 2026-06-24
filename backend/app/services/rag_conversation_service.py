from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


class RAGConversationService:

    @staticmethod
    def build_messages(
        history,
        context: str,
        question: str
    ):
        system_prompt = f"""
            You are a document assistant.

            Rules:

            1. Use ONLY the provided context.
            2. Never invent information.
            3. Cite sources when possible.
            4. If information is missing say:
            "I could not find that information in the uploaded documents."

            Context:

            {context}
            """

        messages = [
            SystemMessage(
                content=system_prompt
            )
        ]

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
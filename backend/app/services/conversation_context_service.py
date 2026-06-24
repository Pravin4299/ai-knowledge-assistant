class ConversationContextService:

    @staticmethod
    def build_history_text(
        messages
    ):

        lines = []

        for msg in messages:

            role = (
                "User"
                if msg.role == "user"
                else "Assistant"
            )

            lines.append(
                f"{role}: {msg.content}"
            )

        return "\n".join(lines)
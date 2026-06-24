from app.services.llm_service import LLMService


# class TitleService:

#     @staticmethod
#     def generate_title(
#         question: str
#     ):

#         prompt = f"""
#         Generate a short title
#         (maximum 6 words).

#         Question:
#         {question}

#         Only return the title.
#         """

#         return (
#             LLMService.generate_text(prompt).strip()
#         )
    



class TitleService:

    @staticmethod
    def generate_title(
        db,
        session,
        question: str
    ):

        prompt = f"""
        Generate a short chat title
        from this user question.

        Question:
        {question}

        Title:
        """

        title = (
            LLMService.generate_text(
                prompt
            )
        )

        session.title = (
            title.strip()[:100]
        )

        db.commit()

        return session.title
class CitationService:

    @staticmethod
    def build_sources(
        chunks
    ):

        seen = set()

        sources = []

        for chunk in chunks:

            key = (
                chunk["document_id"],
                chunk["chunk_index"]
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append(
                {
                    "document_id":
                        chunk["document_id"],

                    "filename":
                        chunk["filename"],

                    "chunk_index":
                        chunk["chunk_index"],

                    "distance":
                        round(
                            chunk.get(
                                "distance",
                                0
                            ),
                            4
                        )
                }
            )

        return sources
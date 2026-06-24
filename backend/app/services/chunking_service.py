from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class ChunkingService:

    CHUNK_SIZE = 700
    CHUNK_OVERLAP = 200

    @staticmethod
    def split_text(
        text: str
    ):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=ChunkingService.CHUNK_SIZE,
            chunk_overlap=ChunkingService.CHUNK_OVERLAP
        )

        return splitter.split_text(text)
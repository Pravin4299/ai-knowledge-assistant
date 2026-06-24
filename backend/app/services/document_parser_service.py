from pypdf import PdfReader
from docx import Document as DocxDocument


class DocumentParserService:

    @staticmethod
    def extract_pdf(file_path: str) -> str:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    @staticmethod
    def extract_docx(file_path: str) -> str:

        doc = DocxDocument(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

    @staticmethod
    def extract_txt(file_path: str) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return file.read()

    @staticmethod
    def extract_text(
        file_path: str,
        file_type: str
    ):

        if file_type == "pdf":
            return DocumentParserService.extract_pdf(
                file_path
            )

        if file_type == "docx":
            return DocumentParserService.extract_docx(
                file_path
            )

        if file_type == "txt":
            return DocumentParserService.extract_txt(
                file_path
            )

        raise ValueError(
            f"Unsupported file type: {file_type}"
        )
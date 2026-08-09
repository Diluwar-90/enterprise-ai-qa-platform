from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


class DocumentParser:
    async def parse(self, file_path: str, content_type: str) -> str:
        path = Path(file_path)

        if content_type == "application/pdf":
            return self._parse_pdf(path)

        if (
            content_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return self._parse_docx(path)

        if content_type == "text/plain":
            return path.read_text(encoding="utf-8")

        raise ValueError(f"Unsupported document type: {content_type}")

    @staticmethod
    def _parse_pdf(path: Path) -> str:
        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages).strip()

    @staticmethod
    def _parse_docx(path: Path) -> str:
        document = DocxDocument(path)

        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n\n".join(paragraphs).strip()
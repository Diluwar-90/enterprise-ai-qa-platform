from pathlib import Path

import pytest

from app.services.document_parser import DocumentParser


@pytest.mark.asyncio
async def test_parse_text_file(tmp_path: Path) -> None:
    file_path = tmp_path / "test.txt"
    file_path.write_text(
        "Enterprise Knowledge Intelligence Platform",
        encoding="utf-8",
    )

    parser = DocumentParser()

    result = await parser.parse(
        str(file_path),
        "text/plain",
    )

    assert result == "Enterprise Knowledge Intelligence Platform"
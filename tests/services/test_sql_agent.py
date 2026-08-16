from unittest.mock import AsyncMock, patch

import pytest

from app.services.sql_agent import SQLAgentService


@pytest.mark.asyncio
async def test_generate_query() -> None:
    service = SQLAgentService()

    with patch.object(
        service.llm,
        "generate",
        new=AsyncMock(
            return_value="SELECT COUNT(*) AS count FROM documents"
        ),
    ) as mock_generate:
        result = await service.generate_query(
            "How many documents are in the system?"
        )

    mock_generate.assert_awaited_once()

    assert result == "SELECT COUNT(*) AS count FROM documents"
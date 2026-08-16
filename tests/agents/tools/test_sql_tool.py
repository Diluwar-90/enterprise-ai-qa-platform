from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.tools.sql import SQLTool


@pytest.mark.asyncio
async def test_sql_tool_executes_select() -> None:
    tool = SQLTool()

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [
        {"count": 5},
    ]

    mock_session = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    mock_session_context = MagicMock()
    mock_session_context.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_context.__aexit__ = AsyncMock(return_value=None)

    with patch(
        "app.agents.tools.sql.AsyncSessionLocal",
        return_value=mock_session_context,
    ):
        result = await tool.execute(
            "SELECT COUNT(*) AS count FROM documents"
        )

    mock_session.execute.assert_awaited_once()
    assert result == "{'count': 5}"


@pytest.mark.asyncio
async def test_sql_tool_rejects_non_select() -> None:
    tool = SQLTool()

    with pytest.raises(
        RuntimeError,
        match="Only SELECT queries are allowed",
    ):
        await tool.execute(
            "DELETE FROM documents"
        )


@pytest.mark.asyncio
async def test_sql_tool_rejects_forbidden_sql() -> None:
    tool = SQLTool()

    with pytest.raises(
        RuntimeError,
        match="Multiple SQL statements are not allowed|Forbidden SQL operation",
    ):
        await tool.execute(
            "SELECT * FROM documents; DROP TABLE documents"
        )


def test_sql_tool_metadata() -> None:
    tool = SQLTool()

    assert tool.name == "sql_query"
    assert "read-only SQL" in tool.description
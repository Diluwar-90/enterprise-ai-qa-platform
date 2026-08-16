import pytest

from app.services.sql_guardrail import SQLGuardrail


def test_allows_select_query() -> None:
    guardrail = SQLGuardrail()

    result = guardrail.validate(
        "SELECT COUNT(*) AS count FROM documents"
    )

    assert result == "SELECT COUNT(*) AS count FROM documents"


def test_allows_trailing_semicolon() -> None:
    guardrail = SQLGuardrail()

    result = guardrail.validate(
        "SELECT COUNT(*) AS count FROM documents;"
    )

    assert result == "SELECT COUNT(*) AS count FROM documents"


@pytest.mark.parametrize(
    "query",
    [
        "INSERT INTO documents (filename) VALUES ('test.txt')",
        "UPDATE documents SET filename = 'test.txt'",
        "DELETE FROM documents",
        "DROP TABLE documents",
        "ALTER TABLE documents ADD COLUMN test TEXT",
        "TRUNCATE documents",
        "CREATE TABLE test (id INTEGER)",
        "GRANT SELECT ON documents TO user",
        "REVOKE SELECT ON documents FROM user",
    ],
)
def test_rejects_write_or_ddl_queries(query: str) -> None:
    guardrail = SQLGuardrail()

    with pytest.raises(
        ValueError,
        match="Only SELECT queries are allowed|Forbidden SQL operation",
    ):
        guardrail.validate(query)


def test_rejects_multiple_statements() -> None:
    guardrail = SQLGuardrail()

    with pytest.raises(
        ValueError,
        match="Multiple SQL statements are not allowed",
    ):
        guardrail.validate(
            "SELECT COUNT(*) FROM documents; DROP TABLE documents"
        )


def test_rejects_embedding_column() -> None:
    guardrail = SQLGuardrail()

    with pytest.raises(
        ValueError,
        match="Access to column 'embedding' is not allowed",
    ):
        guardrail.validate(
            "SELECT embedding FROM document_chunks"
        )


def test_rejects_empty_query() -> None:
    guardrail = SQLGuardrail()

    with pytest.raises(
        ValueError,
        match="SQL query cannot be empty",
    ):
        guardrail.validate("")


def test_rejects_non_select_query() -> None:
    guardrail = SQLGuardrail()

    with pytest.raises(
        ValueError,
        match="Only SELECT queries are allowed",
    ):
        guardrail.validate(
            "WITH data AS (SELECT * FROM documents) DELETE FROM documents"
        )
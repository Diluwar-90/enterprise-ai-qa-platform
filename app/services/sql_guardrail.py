import re


class SQLGuardrail:
    """Validate LLM-generated SQL before database execution."""

    FORBIDDEN_KEYWORDS = (
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke",
    )

    FORBIDDEN_COLUMNS = (
        "embedding",
    )

    def validate(self, query: str) -> str:
        normalized_query = query.strip()

        if not normalized_query:
            raise ValueError("SQL query cannot be empty.")

        # Remove trailing semicolons and whitespace.
        cleaned_query = normalized_query.rstrip(";").strip()

        # Only allow a single SQL statement.
        if ";" in cleaned_query:
            raise ValueError("Multiple SQL statements are not allowed.")

        # Only SELECT queries are allowed.
        if not re.match(r"^select\b", cleaned_query, re.IGNORECASE):
            raise ValueError("Only SELECT queries are allowed.")

        lowered_query = cleaned_query.lower()

        for keyword in self.FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{keyword}\b", lowered_query):
                raise ValueError(
                    f"Forbidden SQL operation: {keyword}."
                )

        for column in self.FORBIDDEN_COLUMNS:
            if re.search(rf"\b{column}\b", lowered_query):
                raise ValueError(
                    f"Access to column '{column}' is not allowed."
                )

        return cleaned_query
from dataclasses import dataclass
from typing import Literal

ActionType = Literal[
    "sql_read",
    "sensitive_data_access",
    "sql_write",
]


@dataclass(frozen=True)
class ActionClassification:
    action: ActionType
    reason: str


class ActionClassifier:
    SENSITIVE_COLUMNS = (
        "email",
        "storage_path",
        "error_message",
    )

    def classify_sql(self, query: str) -> ActionClassification:
        normalized_query = query.lower()

        if any(
            column in normalized_query
            for column in self.SENSITIVE_COLUMNS
        ):
            return ActionClassification(
                action="sensitive_data_access",
                reason="The query requests potentially sensitive data.",
            )

        return ActionClassification(
            action="sql_read",
            reason="The query is a standard read-only database operation.",
        )
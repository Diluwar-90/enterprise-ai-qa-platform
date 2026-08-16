from dataclasses import dataclass
from typing import Literal

Route = Literal["knowledge", "sql", "direct",  "blocked",]

ActionType = Literal[
    "sql_read",
    "sensitive_data_access",
    "sql_write",
]

@dataclass
class AgentState:
    query: str
    route: Route | None = None
    context: str = ""
    sql_query: str = ""
    sql_result: str = ""
    action: ActionType | None = None
    approval_required: bool = False
    approval_status: str = "not_required"
    answer: str = ""
    error: str = ""
from dataclasses import dataclass
from typing import Literal

Route = Literal["knowledge", "direct"]

@dataclass
class AgentState:
    query: str
    route: Route | None = None
    context: str = ""
    answer: str = ""
    error: str = ""
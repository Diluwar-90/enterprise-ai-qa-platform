from dataclasses import dataclass


@dataclass
class AgentState:
    query: str
    route: str = ""
    context: str = ""
    answer: str = ""
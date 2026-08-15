from langgraph.graph import END, START, StateGraph

from app.agents.nodes import AgentNodes
from app.agents.state import AgentState


def build_agent_graph():
    nodes = AgentNodes()

    graph = StateGraph(AgentState)

    graph.add_node("route", nodes.route)
    graph.add_node("retrieve", nodes.retrieve)
    graph.add_node("generate", nodes.generate)

    graph.add_edge(START, "route")

    graph.add_conditional_edges(
        "route",
        lambda state: state.route,
        {
            "knowledge": "retrieve",
            "direct": "generate",
        },
    )

    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
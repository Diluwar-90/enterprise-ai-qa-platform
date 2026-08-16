from langgraph.graph import END, START, StateGraph

from app.agents.nodes import AgentNodes
from app.agents.state import AgentState


def build_agent_graph():
    nodes = AgentNodes()

    graph = StateGraph(AgentState)

    graph.add_node("route", nodes.route)
    graph.add_node("retrieve", nodes.retrieve)
    graph.add_node("generate_sql", nodes.generate_sql)
    graph.add_node("classify_sql_action", nodes.classify_sql_action)
    graph.add_node("check_approval", nodes.check_approval)
    graph.add_node("sql_execute", nodes.sql_execute)
    graph.add_node("generate", nodes.generate)

    graph.add_edge(START, "route")

    graph.add_conditional_edges(
        "route",
        lambda state: state.route,
        {
            "knowledge": "retrieve",
            "sql": "generate_sql",
            "direct": "generate",
        },
    )

    # Knowledge/RAG path
    graph.add_edge("retrieve", "generate")

    # SQL path
    graph.add_edge("generate_sql", "classify_sql_action")
    graph.add_edge("classify_sql_action", "check_approval")

    def route_after_approval(state: AgentState) -> str:
        if state.approval_required:
            return "pending"

        return "execute"

    graph.add_conditional_edges(
        "check_approval",
        route_after_approval,
        {
            "pending": END,
            "execute": "sql_execute",
        },
    )

    graph.add_edge("sql_execute", "generate")

    # Final response
    graph.add_edge("generate", END)

    return graph.compile()
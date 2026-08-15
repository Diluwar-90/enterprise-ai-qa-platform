from app.agents.state import AgentState
from app.services.llm import LLMService
from app.services.retrieval import RetrievalService


class AgentNodes:
    def __init__(self) -> None:
        self.retrieval = RetrievalService()
        self.llm = LLMService()

    async def retrieve(self, state: AgentState) -> AgentState:
        result = await self.retrieval.retrieve_hybrid(
            query=state.query,
            limit=5,
        )

        state.context = result.context

        return {
             "context": result.context,
        }

    async def generate(self, state: AgentState) -> AgentState:
        if state.route == "knowledge" and not state.context.strip():
            answer = "I do not have enough information to answer."
            return {
                "answer":answer
            }

        prompt = f"""
    You are an enterprise knowledge assistant.

    Answer the user's question using ONLY the provided context.

    Rules:
    1. Do not use information that is not present in the context.
    2. Do not invent or assume facts.
    3. If the context does not contain enough information to answer,
        respond exactly:
        "I do not have enough information to answer."
    4. Give a clear and concise answer.

    Context:
    {state.context}

    Question:
    {state.query}
    """

        answer = await self.llm.generate(prompt)

        return {
             "answer": answer,
        }

    def route(self, state: AgentState) -> AgentState:
        knowledge_keywords = (
            "what",
            "who",
            "where",
            "when",
            "how",
            "why",
            "explain",
            "describe",
            "tell me",
        )

        query = state.query.lower().strip()

        if query.startswith(knowledge_keywords):
            route = "knowledge"
        else:
            route = "direct"

        return {"route": route}

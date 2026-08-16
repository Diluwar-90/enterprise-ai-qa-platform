from app.agents.state import AgentState
from app.agents.tools.retrieval import RetrievalTool
from app.agents.tools.sql import SQLTool
from app.services.action_classifier import ActionClassifier
from app.services.llm import LLMService
from app.services.sql_agent import SQLAgentService


class AgentNodes:
    def __init__(self) -> None:
        self.retrieval = RetrievalTool()
        self.sql = SQLTool()
        self.sql_agent = SQLAgentService()
        self.action_classifier = ActionClassifier()
        self.llm = LLMService()

    async def retrieve(self, state: AgentState) -> AgentState:
        try:
            context = await self.retrieval.search(
                query=state.query,
                limit=5,
            )
        except RuntimeError as exc:
            return {
                "context": "",
                "error": str(exc),
            }

        return {
            "context": context,
        }

    async def generate(self, state: AgentState) -> AgentState:
        if state.error:
            return {
                "answer": "Unable to retrieve knowledge at this time.",
            }

        if state.route == "sql":
            if not state.sql_result.strip():
                return {
                    "answer": "No database result was available.",
                }

            prompt = f"""
You are an enterprise data assistant.

Answer the user's question using ONLY the database result provided.

Rules:
1. Do not invent information.
2. Do not expose the SQL query unless the user asks for it.
3. Give a clear and concise answer.
4. Use the exact values from the database result.

Database result:
{state.sql_result}

Question:
{state.query}
"""

            answer = await self.llm.generate(prompt)

            return {
                "answer": answer,
            }

        if state.route == "knowledge" and not state.context.strip():
            return {
                "answer": "I do not have enough information to answer.",
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
        query = state.query.lower().strip()

        sql_keywords = (
            "count",
            "how many",
            "number of",
            "list",
            "show",
            "total",
            "database",
            "records",
            "users",
            "documents",
        )

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

        destructive_keywords = (
            "delete",
            "remove",
            "drop",
            "truncate",
            "destroy",
            "erase",
            "modify",
            "change",
            "update",
            "insert",
            "alter",
            "create",
        )

        if any(keyword in query for keyword in destructive_keywords):
            route = "blocked"
        elif any(keyword in query for keyword in sql_keywords):
            route = "sql"
        elif query.startswith(knowledge_keywords):
            route = "knowledge"
        else:
            route = "direct"

        return {"route": route}

    async def sql_execute(self, state: AgentState) -> AgentState:
        try:
            result = await self.sql.execute(state.sql_query)
        except RuntimeError as exc:
            return {
                "sql_result": "",
                "error": str(exc),
            }

        return {
            "sql_result": result,
        }

    async def generate_sql(self, state: AgentState) -> AgentState:
        try:
            sql_query = await self.sql_agent.generate_query(
                state.query
            )
        except RuntimeError as exc:
            return {
                "sql_query": "",
                "error": f"SQL query generation failed: {exc}",
            }

        return {
            "sql_query": sql_query,
        }

    async def classify_sql_action(
        self,
        state: AgentState,
    ) -> AgentState:
        try:
            classification = self.action_classifier.classify_sql(
                state.sql_query
            )
        except ValueError as exc:
            return {
                "error": f"SQL action classification failed: {exc}",
            }

        return {
            "action": classification.action,
        }

    def check_approval(self, state: AgentState) -> AgentState:
        if state.action == "sensitive_data_access":
            return {
                "approval_required": True,
                "approval_status": "pending",
                "answer": (
                    "Human approval is required before accessing "
                    "sensitive data."
                ),
            }

        return {
            "approval_required": False,
            "approval_status": "not_required",
        }

    def blocked(self, state: AgentState) -> AgentState:
        return {
            "answer": (
                "I cannot perform database modification or destructive "
                "operations."
            ),
            "error": "Destructive database operation blocked.",
        }
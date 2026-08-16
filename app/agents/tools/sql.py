from sqlalchemy import text

from app.db.session import AsyncSessionLocal
from app.services.sql_guardrail import SQLGuardrail


class SQLTool:
    name = "sql_query"
    description = (
        "Execute a read-only SQL query against the enterprise database "
        "and return the results."
    )

    def __init__(self) -> None:
        self.guardrail = SQLGuardrail()

    async def execute(self, query: str) -> str:
        try:
            safe_query = self.guardrail.validate(query)

            async with AsyncSessionLocal() as session:
                result = await session.execute(text(safe_query))
                rows = result.mappings().all()

            if not rows:
                return "No results found."

            return "\n".join(str(dict(row)) for row in rows)

        except ValueError as exc:
            raise RuntimeError(str(exc)) from exc

        except Exception as exc:
            raise RuntimeError("SQL tool execution failed.") from exc
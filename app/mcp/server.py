from mcp.server.mcpserver import MCPServer

from app.agents.tools.retrieval import RetrievalTool
from app.agents.tools.sql import SQLTool
import asyncio


server = MCPServer(
    name="enterprise-knowledge-intelligence",
    title="Enterprise Knowledge Intelligence MCP Server",
    description=(
        "MCP server exposing enterprise knowledge retrieval "
        "and read-only SQL capabilities."
    ),
    version="1.0.0",
)


retrieval_tool = RetrievalTool()
sql_tool = SQLTool()


@server.tool(
    name="knowledge_search",
    title="Knowledge Search",
    description=(
        "Search enterprise knowledge and retrieve relevant "
        "document context using the existing hybrid retrieval pipeline."
    ),
)
async def knowledge_search(
    query: str,
    limit: int = 5,
) -> str:
    """Search enterprise knowledge."""
    return await retrieval_tool.search(
        query=query,
        limit=limit,
    )


@server.tool(
    name="sql_query",
    title="Read-only SQL Query",
    description=(
        "Execute a read-only SQL query against the enterprise database. "
        "Queries are validated by the SQL guardrail before execution."
    ),
)
async def sql_query(query: str) -> str:
    """Execute a guarded read-only SQL query."""
    return await sql_tool.execute(query=query)


if __name__ == "__main__":
    asyncio.run(
        server.run_streamable_http_async(
            host="127.0.0.1",
            port=8000,
            streamable_http_path="/mcp",
        )
    )
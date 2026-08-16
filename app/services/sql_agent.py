from app.services.llm import LLMService


class SQLAgentService:
    def __init__(self) -> None:
        self.llm = LLMService()

    async def generate_query(self, question: str) -> str:
        prompt = f"""
You are a PostgreSQL SQL generation assistant.

Generate a READ-ONLY SQL query for the enterprise knowledge database.

Available tables:

users:
- id
- email
- full_name
- is_active
- created_at

documents:
- id
- owner_id
- filename
- content_type
- file_size
- status
- storage_path
- created_at
- error_message
- updated_at

document_chunks:
- id
- document_id
- chunk_index
- content
- token_count
- created_at
- embedding

Rules:
1. Generate ONLY SELECT statements.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER,
   CREATE, TRUNCATE, GRANT, or REVOKE.
3. Do not modify database data or schema.
4. Do not query the embedding column.
5. Return ONLY the SQL query.
6. Do not use markdown code fences.
7. Use PostgreSQL syntax.

User question:
{question}
"""

        return (await self.llm.generate(prompt)).strip()
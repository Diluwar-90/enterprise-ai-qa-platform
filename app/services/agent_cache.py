import hashlib


class AgentCache:
    PREFIX = "agent:response:"
    TTL_SECONDS = 300

    @classmethod
    def build_key(cls, query: str) -> str:
        normalized_query = " ".join(query.strip().lower().split())
        query_hash = hashlib.sha256(
            normalized_query.encode("utf-8")
        ).hexdigest()

        return f"{cls.PREFIX}{query_hash}"

    @classmethod
    def should_cache(cls, result: dict) -> bool:
        return (
            result.get("approval_required") is False
            and result.get("action") == "sql_read"
            and bool(result.get("answer"))
        )
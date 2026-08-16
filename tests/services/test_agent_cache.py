from app.services.agent_cache import AgentCache


def test_build_key_is_deterministic() -> None:
    key1 = AgentCache.build_key(
        "How many documents are in the system?"
    )
    key2 = AgentCache.build_key(
        "  how   many documents are in the system?  "
    )

    assert key1 == key2
    assert key1.startswith("agent:response:")


def test_should_cache_normal_response() -> None:
    result = {
        "answer": "There are 5 documents.",
        "approval_required": False,
        "approval_status": "not_required",
        "action": "sql_read",
    }

    assert AgentCache.should_cache(result) is True


def test_should_not_cache_sensitive_response() -> None:
    result = {
        "answer": "Human approval is required.",
        "approval_required": True,
        "approval_status": "pending",
        "action": "sensitive_data_access",
    }

    assert AgentCache.should_cache(result) is False


def test_should_not_cache_blocked_response() -> None:
    result = {
        "answer": (
            "I cannot perform database modification or destructive operations."
        ),
        "approval_required": False,
        "approval_status": "not_required",
        "action": None,
    }

    assert AgentCache.should_cache(result) is False
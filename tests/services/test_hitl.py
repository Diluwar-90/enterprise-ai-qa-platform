import pytest

from app.services.hitl import HITLService


def test_sql_write_requires_approval() -> None:
    service = HITLService()

    assert service.requires_approval("sql_write") is True


def test_sensitive_data_requires_approval() -> None:
    service = HITLService()

    assert service.requires_approval("sensitive_data_access") is True


def test_read_only_sql_does_not_require_approval() -> None:
    service = HITLService()

    assert service.requires_approval("sql_read") is False


def test_create_approval_request() -> None:
    service = HITLService()

    request = service.create_request(
        action="sql_write",
        reason="The requested operation modifies database records.",
    )

    assert request.action == "sql_write"
    assert request.reason == (
        "The requested operation modifies database records."
    )


def test_create_request_rejects_unnecessary_approval() -> None:
    service = HITLService()

    with pytest.raises(
        ValueError,
        match="Approval is not required",
    ):
        service.create_request(
            action="sql_read",
            reason="Read-only query.",
        )
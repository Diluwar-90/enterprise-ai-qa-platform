from app.services.action_classifier import ActionClassifier


def test_classifies_normal_sql_read() -> None:
    classifier = ActionClassifier()

    result = classifier.classify_sql(
        "SELECT COUNT(*) FROM documents"
    )

    assert result.action == "sql_read"
    assert "standard read-only" in result.reason


def test_classifies_email_access_as_sensitive() -> None:
    classifier = ActionClassifier()

    result = classifier.classify_sql(
        "SELECT email FROM users"
    )

    assert result.action == "sensitive_data_access"


def test_classifies_storage_path_as_sensitive() -> None:
    classifier = ActionClassifier()

    result = classifier.classify_sql(
        "SELECT storage_path FROM documents"
    )

    assert result.action == "sensitive_data_access"


def test_classifies_error_message_as_sensitive() -> None:
    classifier = ActionClassifier()

    result = classifier.classify_sql(
        "SELECT error_message FROM documents"
    )

    assert result.action == "sensitive_data_access"
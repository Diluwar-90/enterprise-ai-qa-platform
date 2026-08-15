class AppException(Exception):
    """Base exception for application-level errors."""


class AgentExecutionError(AppException):
    """Raised when agent execution fails."""
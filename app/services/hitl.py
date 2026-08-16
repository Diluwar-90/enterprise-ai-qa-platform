from dataclasses import dataclass


@dataclass
class ApprovalRequest:
    action: str
    reason: str


class HITLService:
    def requires_approval(self, action: str) -> bool:
        return action in {
            "sql_write",
            "sensitive_data_access",
        }

    def create_request(
        self,
        action: str,
        reason: str,
    ) -> ApprovalRequest:
        if not self.requires_approval(action):
            raise ValueError(
                f"Approval is not required for action '{action}'."
            )

        return ApprovalRequest(
            action=action,
            reason=reason,
        )
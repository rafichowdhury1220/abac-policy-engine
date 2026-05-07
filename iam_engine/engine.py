from typing import Dict, List, Tuple

from iam_engine.attribute_store import AttributeStore
from iam_engine.policy import Policy

class PolicyDecision:
    def __init__(self, allowed: bool, reason: str, matched_policies: List[str]):
        self.allowed = allowed
        self.reason = reason
        self.matched_policies = matched_policies

    def __repr__(self) -> str:
        return f"PolicyDecision(allowed={self.allowed}, reason={self.reason}, matched_policies={self.matched_policies})"

class PolicyEngine:
    def __init__(self, policies: List[Policy], store: AttributeStore):
        self.policies = policies
        self.store = store

    def evaluate(self, user_id: str, resource_id: str, action: str) -> PolicyDecision:
        context = self.store.get_context(user_id, resource_id, action)
        allow_matches: List[str] = []
        deny_matches: List[str] = []

        for policy in self.policies:
            for rule in policy.rules:
                if rule.matches(context):
                    if rule.effect == "deny":
                        deny_matches.append(policy.policy_id)
                    elif rule.effect == "allow":
                        allow_matches.append(policy.policy_id)

        if deny_matches:
            return PolicyDecision(False, "Explicit deny match", deny_matches)
        if allow_matches:
            return PolicyDecision(True, "Allow match", allow_matches)
        return PolicyDecision(False, "Default deny", [])

    def explain(self, user_id: str, resource_id: str, action: str) -> Tuple[Dict[str, str], PolicyDecision]:
        decision = self.evaluate(user_id, resource_id, action)
        return ({
            "user_id": user_id,
            "resource_id": resource_id,
            "action": action,
        }, decision)

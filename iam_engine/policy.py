from typing import Any, Dict, List, Optional

class Condition:
    def __init__(self, attribute: str, operator: str, value: Any):
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def evaluate(self, context: Dict[str, Any]) -> bool:
        actual = context.get(self.attribute)
        if self.operator == "==":
            return actual == self.value
        if self.operator == "!=":
            return actual != self.value
        if self.operator == "in":
            return actual in self.value
        if self.operator == "not in":
            return actual not in self.value
        if self.operator == ">":
            return actual > self.value
        if self.operator == ">=":
            return actual >= self.value
        if self.operator == "<":
            return actual < self.value
        if self.operator == "<=":
            return actual <= self.value
        raise ValueError(f"Unsupported operator: {self.operator}")

    def __repr__(self) -> str:
        return f"Condition({self.attribute} {self.operator} {self.value})"

class PolicyRule:
    def __init__(self, effect: str, conditions: List[Condition], description: Optional[str] = None):
        self.effect = effect.lower()
        self.conditions = conditions
        self.description = description or ""

    def matches(self, context: Dict[str, Any]) -> bool:
        return all(condition.evaluate(context) for condition in self.conditions)

    def __repr__(self) -> str:
        return f"PolicyRule(effect={self.effect}, conditions={self.conditions})"

class Policy:
    def __init__(self, policy_id: str, rules: List[PolicyRule], description: Optional[str] = None):
        self.policy_id = policy_id
        self.rules = rules
        self.description = description or ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Policy":
        rules = []
        for rule_data in data.get("rules", []):
            conditions = [
                Condition(cond["attribute"], cond["operator"], cond["value"])
                for cond in rule_data.get("conditions", [])
            ]
            rules.append(PolicyRule(rule_data["effect"], conditions, rule_data.get("description")))
        return cls(data["policy_id"], rules, data.get("description"))

    def __repr__(self) -> str:
        return f"Policy(policy_id={self.policy_id}, rules={self.rules})"

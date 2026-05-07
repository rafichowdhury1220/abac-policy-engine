from typing import Any, Dict

class AttributeStore:
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.environment: Dict[str, Any] = {}

    def add_user(self, user_id: str, attributes: Dict[str, Any]) -> None:
        self.users[user_id] = attributes

    def add_resource(self, resource_id: str, attributes: Dict[str, Any]) -> None:
        self.resources[resource_id] = attributes

    def set_environment(self, environment: Dict[str, Any]) -> None:
        self.environment = environment

    def get_context(self, user_id: str, resource_id: str, action: str) -> Dict[str, Any]:
        context = {
            "user.id": user_id,
            "resource.id": resource_id,
            "action": action,
        }
        context.update({f"user.{k}": v for k, v in self.users.get(user_id, {}).items()})
        context.update({f"resource.{k}": v for k, v in self.resources.get(resource_id, {}).items()})
        context.update({f"environment.{k}": v for k, v in self.environment.items()})
        return context

    def __repr__(self) -> str:
        return f"AttributeStore(users={list(self.users.keys())}, resources={list(self.resources.keys())})"

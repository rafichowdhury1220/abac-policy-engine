from iam_engine.attribute_store import AttributeStore
from iam_engine.engine import PolicyEngine
from iam_engine.policy import Policy

POLICIES = [
    {
        "policy_id": "finance-network-access",
        "description": "Allow finance users on trusted corporate network to access finance resources.",
        "rules": [
            {
                "effect": "allow",
                "description": "Finance users on trusted network can access finance resources.",
                "conditions": [
                    {"attribute": "user.department", "operator": "==", "value": "finance"},
                    {"attribute": "resource.type", "operator": "==", "value": "finance_document"},
                    {"attribute": "environment.network", "operator": "==", "value": "corporate"},
                    {"attribute": "user.device_trusted", "operator": "==", "value": True},
                ],
            }
        ],
    },
    {
        "policy_id": "deny-externals",
        "description": "Deny external contractors from internal systems during business hours.",
        "rules": [
            {
                "effect": "deny",
                "description": "Block contractors on internal resources while business hours are active.",
                "conditions": [
                    {"attribute": "user.role", "operator": "==", "value": "contractor"},
                    {"attribute": "resource.sensitivity", "operator": "==", "value": "internal"},
                    {"attribute": "environment.time_of_day", "operator": "in", "value": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]},
                ],
            }
        ],
    },
    {
        "policy_id": "senior-engineer-document-access",
        "description": "Allow senior engineers to view public architecture resources.",
        "rules": [
            {
                "effect": "allow",
                "conditions": [
                    {"attribute": "user.title", "operator": "==", "value": "senior_engineer"},
                    {"attribute": "resource.sensitivity", "operator": "==", "value": "public"},
                    {"attribute": "action", "operator": "==", "value": "read"},
                ],
            }
        ],
    },
]

REQUESTS = [
    {"user_id": "u100", "resource_id": "r_finance", "action": "read"},
    {"user_id": "u200", "resource_id": "r_internal", "action": "write"},
    {"user_id": "u300", "resource_id": "r_public", "action": "read"},
]


def build_attribute_store() -> AttributeStore:
    store = AttributeStore()
    store.add_user("u100", {
        "department": "finance",
 "role": "employee",
        "device_trusted": True,
        "title": "finance_analyst",
    })
    store.add_user("u200", {
        "department": "engineering",
        "role": "contractor",
        "device_trusted": False,
        "title": "consultant",
    })
    store.add_user("u300", {
        "department": "engineering",
        "role": "employee",
        "device_trusted": True,
        "title": "senior_engineer",
    })

    store.add_resource("r_finance", {
        "type": "finance_document",
        "sensitivity": "confidential",
    })
    store.add_resource("r_internal", {
        "type": "service_console",
        "sensitivity": "internal",
    })
    store.add_resource("r_public", {
        "type": "architecture_document",
        "sensitivity": "public",
    })

    store.set_environment({
        "network": "corporate",
        "time_of_day": "10:00",
    })
    return store


def main() -> None:
    store = build_attribute_store()
    policies = [Policy.from_dict(data) for data in POLICIES]
    engine = PolicyEngine(policies, store)

    print("IAM/ABAC Evaluation Demo")
    print("========================\n")

    for request in REQUESTS:
        decision = engine.evaluate(request["user_id"], request["resource_id"], request["action"])
        context = store.get_context(request["user_id"], request["resource_id"], request["action"])

        print(f"Request: user={request['user_id']}, resource={request['resource_id']}, action={request['action']}")
        print("Context:")
        for key, value in context.items():
            print(f"  {key} = {value}")
        print(f"Decision: {'ALLOW' if decision.allowed else 'DENY'}")
        print(f"Reason: {decision.reason}")
        print(f"Matched policies: {decision.matched_policies}\n")

    print("Architecture note: This demo separates attributes, policies, and evaluation to mirror an IAM engine and solution architect design.")


if __name__ == "__main__":
    main()

# ABAC Policy Engine

A sample Python project demonstrating the capabilities of an IAM engineer and solution architect through an attribute-based access control (ABAC) engine.

## What this project shows

- Policy authoring and evaluation using attributes
- Attribute store design for users, resources, and environment
- Policy decision engine with deny/allow precedence
- Solution architecture considerations for IAM services
- Example request evaluation scenarios and integration patterns

## Key components

- `iam_engine/policy.py`: policy model and condition evaluation
- `iam_engine/attribute_store.py`: attribute data store and context builder
- `iam_engine/engine.py`: policy evaluation engine and decision flow
- `examples/main.py`: runnable demonstration for IAM scenarios
- `docs/architecture.md`: architecture overview for IAM/systems design

## Run the example

```bash
python examples/main.py
```

## Architecture summary

This project is designed to reflect an IAM solution architect's view:

- Policies are first-class artifacts and are evaluated at runtime
- Attributes are separated by identity, resource, and environment
- The engine supports extensible condition operators and decision logic
- The system is easily adapted into a middleware, microservice, or API gateway

## Notes for engineers

- Implement this pattern in production with persistent attribute stores, logging, metrics, and policy lifecycle management.
- Use a JSON/YAML policy catalog and a policy evaluation service for centralized authorization.
- Keep authorization decisions deterministic and auditable.

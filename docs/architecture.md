# IAM Engine Solution Architecture

## Overview

This sample project demonstrates a small-scale IAM authorization engine built with attribute-based access control (ABAC). It is intended to reflect both engineering and solution architecture capabilities:

- IAM engineer: policy modeling, attribute store design, runtime evaluation, explicit deny precedence.
- Solution architect: system decomposition, integration patterns, auditability, and extensibility.

## Components

1. `AttributeStore`
   - Captures identity, resource, and environment attributes.
   - Provides a unified request context for authorization decisions.

2. `Policy` and `PolicyRule`
   - Represent declarative authorization rules.
   - Support multiple operators and flexible attribute comparisons.

3. `PolicyEngine`
   - Evaluates request context against policies.
   - Applies deny-before-allow semantics.
   - Returns decision reason and matched policies for observability.

## Design patterns

- Separation of concerns: keep attribute ingestion separate from policy evaluation.
- Policy-as-data: store rules externally so they can be changed without code updates.
- Explicit deny: deny rules always override allow rules, supporting safe default-deny behavior.

## Deployment / integration ideas

- Middleware: integrate `PolicyEngine` into a web API gateway or service authorization layer.
- Microservice: expose policy evaluation via REST or gRPC, backed by a central attribute store.
- CI/CD: generate policy catalogs and validate policies as part of deployment pipelines.

## Example scenarios covered

- Finance users can access finance documents only from trusted corporate network.
- Contractors are denied access to internal resources during business hours.
- Senior engineers can read public architecture documents.

## Architecture considerations

- Auditability: log policy decisions, matched policy IDs, and request context.
- Attribute refresh: keep identity/resource/environment data up to date from HR, CMDB, and network systems.
- Policy lifecycle: provide authoring, review, staging, and production promotion for policies.
- Scalability: scale evaluation horizontally and cache attribute contexts where safe.

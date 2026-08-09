# Guided Practice 12 – Conduct an Architecture Review

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Artefact Reference:** [`docs/artefacts/day-12-design-proposal.md`](../artefacts/day-12-design-proposal.md)  
**Time Spent:** ~90 minutes (Architectural Design Document Evaluation)

---

## 🏢 Engineering Scenario & Review Scope
> "Tomorrow morning your team's design proposal—'Bookstore Orders & Notification Service v1'—will be presented to the Architecture Review Board (ARB). Your Tech Lead asks you to conduct the initial architecture review. Your responsibility is to evaluate architectural trade-offs, identify hidden operational risks, challenge assumptions, and determine whether the proposal is ready to proceed to implementation."

---

## 🔍 Proposal Architecture Evaluation

### Key Architecture Components Assessed:
- **Service Boundaries:** Proposed decoupling Order handling and Notification dispatch into separate microservices.
- **Data Model Strategy:** Proposed sharing a single relational database (`bookstore_db`) between Order Service and Catalog Service during v1.
- **Payment Processing:** Proposed synchronous REST HTTP call from Order Service to external Payment Gateway.
- **Event Messaging:** Proposed publishing `order-placed` events directly to Apache Kafka topics after database save.

---

## ⚠️ Architectural Risks & Hidden Assumptions

| Risk / Assumption # | Architecture Area | Problem Description | Production Risk Level |
|---|---|---|---|
| **Risk 1** | **Shared Database Anti-Pattern** | Proposal shares a single database schema between Order Service and Catalog Service. | **HIGH (Blocking)** |
| **Risk 2** | **Synchronous Uncompensated Payment Call** | Order Service makes a synchronous HTTP call to Payment Gateway. If payment times out after database stock deduction, reserved stock is left locked in a dirty state. | **HIGH (Blocking)** |
| **Risk 3** | **Dual-Write Without Transactional Outbox** | Proposal writes to Database first, then attempts to publish to Kafka. If Kafka is down or network blips occur, the database commit succeeds but the message is lost forever (Dual-Write Failure). | **HIGH (Blocking)** |
| **Risk 4** | **Unclear PCI / PII Boundary** | Proposal does not explicitly restrict credit card data logging or customer PII sanitization in order payloads. | **MEDIUM** |
| **Risk 5** | **Missing Idempotency Strategy** | `POST /api/orders` lacks idempotency key enforcement. Network retries from mobile clients will create duplicate orders and double-charge customers. | **HIGH (Blocking)** |

---

## 💡 Review Questions for the Proposal Author

1. **Idempotency:** How does `POST /api/orders` handle client network retries? Will duplicate requests with the same idempotency key return the existing order or create a second charge?
2. **Payment Failure Compensation:** If the Payment Gateway times out after 5000ms, how is reserved inventory released back to stock?
3. **Dual-Write Safety:** What happens if `order-placed` fails to publish to Kafka after the database transaction commits? How are lost events detected and replayed?
4. **Database Ownership & Schema Migrations:** Who owns database schema migrations on the shared `bookstore_db` database? How will schema changes in Catalog Service avoid breaking Order Service queries?

---

## 🚦 Architectural Review Decision

### Final Recommendation: **APPROVE WITH REQUIRED CHANGES**

#### Required Architectural Changes Before Proceeding to Build:

```text
REQUIRED CHANGES (Must be updated in Design Doc before approval):
  1. Add Transactional Outbox Pattern (or CDC / Debezium) for Kafka event publishing to solve dual-write message loss.
  2. Implement Idempotency Key header ('X-Idempotency-Key') on POST /api/orders.
  3. Define Inventory Compensation / Rollback logic for payment timeouts.
  4. Specify explicit ownership boundary for shared database schema OR establish a strict timeline for database decoupling.
  5. Add explicit PII/PCI logging suppression rules in Order Service filters.
```

---

## ✅ Self-Check & Completion Sign-Off
- [x] Challenged design assumptions respectfully using architectural principles.
- [x] Balanced product delivery timelines against engineering scalability, security, and operational reliability.
- [x] Identified high-risk architectural anti-patterns (Shared DB, Dual-Write failure, Missing Idempotency).
- [x] Recommended a clear ARB outcome (**Approve with Required Changes**) without prematurely forcing a complete redesign.
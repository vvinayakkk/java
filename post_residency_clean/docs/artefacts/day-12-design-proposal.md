# Day 12 Artefact — Design Proposal (Draft)

**Title:** Bookstore Orders & Notification Service (v1)  
**Authors:** Bookstore Platform Team (draft)  
**Status:** Draft for Architecture Review Board  
**Reviewer (you):** Perform readiness review — do **not** redesign.

---

## 1. Problem

Customers can browse books via the existing REST API, but purchasing requires leaving the system for a third-party form. Support reports lost conversions. Product wants **in-app checkout** with email confirmation within one quarter.

## 2. Goals

- Accept an order for one or more books (ISBN + quantity)
- Reserve stock atomically
- Return order id within 500ms p95 at 50 RPS
- Email order confirmation within 2 minutes
- Keep existing Book/Author/Category APIs stable

## 3. Non-goals

- Multi-warehouse inventory
- Payment gateway abstraction beyond one provider
- Mobile offline checkout
- International tax engine

## 4. Constraints

| Constraint | Detail |
|------------|--------|
| Team | 3 backend engineers, 1 SRE (20%) |
| Runtime | Spring Boot services on Kubernetes (2 regions planned “later”) |
| Data | PostgreSQL primary (bookstore DB will be reused) |
| Timeline | 6 weeks to beta |
| Compliance | Must not store raw card data (PCI) |

## 5. Proposed architecture

```text
Mobile/Web
  → API Gateway
    → Order Service (new)
         → Bookstore DB (shared with Catalog Service)  ★
         → Payment Provider (sync HTTP)
         → Kafka topic `order-placed`
              → Notification Service (email)
              → Analytics Consumer
```

### Key decisions

1. **Shared database** between Catalog (existing bookstore app) and new Order Service to “move fast.”
2. **Synchronous payment** inside the order request before HTTP 201.
3. **Kafka** for email/analytics after order commit.
4. **Stock reservation** via `UPDATE books SET stock = stock - ? WHERE id = ? AND stock >= ?` in Order Service.
5. **No saga / outbox** in v1 — “we’ll add if needed.”
6. **Feature flag** for gradual rollout to 10% of users.

## 6. API sketch

```http
POST /api/orders
{
  "customerEmail": "a@b.com",
  "items": [{"bookId": 1, "quantity": 2}]
}
→ 201 { "orderId": "...", "status": "PAID" }
```

## 7. Stakeholder comments (pre-review)

| Who | Comment |
|-----|---------|
| Product | “Shared DB is fine if it ships this quarter.” |
| SRE | “Sync payment + shared DB makes failure modes scary. Where is rollback?” |
| Security | “Email in logs? Card token handling unclear.” |
| Data | “Analytics consumer will want PII — governance?” |

## 8. Open questions from authors

- Is Redis needed for idempotency keys?
- Should Notification Service own email templates?
- Do we need multi-region in year one?

## 9. Success metrics

- Checkout conversion +15%
- Order p95 < 500ms
- Email success > 99%

## 10. What you must produce

Architecture Review Recommendation: assumptions, risks, trade-offs, questions, blocking concerns, positives, and **Approve / Approve with Required Changes / Reject Pending Rework**.

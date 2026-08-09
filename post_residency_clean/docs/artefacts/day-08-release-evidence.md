# Day 8 Artefact — Release Evidence Pack

Tomorrow morning the team plans to deploy a new bookstore feature. Dev and QA signed off. Product wants schedule kept for a customer commitment. **You** perform the final Engineering Readiness Review.

---

## Information available

### Green

- Performance testing passed
- Load testing passed
- Automated tests: **98%** pass rate
- Comprehensive application logging

### Yellow / warnings

- Monitoring lacks **business metrics** and **alert thresholds**
- Rollback procedure exists but has **never been tested**
- One deployment configuration still requires **manual editing**
- A **medium-risk dependency vulnerability** is awaiting a vendor patch

---

## Feature under review (context)

“Book Recommendations v1” — new endpoint returning related books; uses the Day-5 cache and depends on catalog sync freshness from Day 6.

---

## Your decision options (exactly one)

1. **Approve**
2. **Approve with Conditions**
3. **Reject**

Support every decision with engineering evidence from this pack.

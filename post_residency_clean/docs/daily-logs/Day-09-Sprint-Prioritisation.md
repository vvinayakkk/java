# Guided Practice 9 – Sprint Prioritisation

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Artefact Reference:** [`docs/artefacts/day-09-backlog.md`](../artefacts/day-09-backlog.md)  
**Time Spent:** ~80 minutes (Backlog Prioritization & Stakeholder Trade-off Defense)  
**Engineering Capacity Cap:** **16 Story Points (SP)**

---

## 🏢 Engineering Scenario & Stakeholder Context
> "You inherit a core production service where customer reliability is burning: checkout timeouts generate 400 support tickets/week, security mandates a CVE patch, SRE reports the error budget is nearly exhausted, while Product leadership demands Feature A (8 SP) for a key enterprise customer. You must build a realistic sprint proposal capped at 16 Story Points and defend your trade-offs."

---

## 📊 Backlog Item Evaluation & Selection

### Total Backlog Capacity: **16 Story Points Max**

| Item # | Backlog Description | Story Points | Impact Category | Priority Justification | Action |
|---|---|---|---|---|---|
| **1** | **Fix intermittent checkout timeout** | **5 SP** | Customer / Revenue | 400 support tickets/week. Direct revenue loss. Must fix immediately to protect error budget. | **SELECTED** |
| **2** | **Upgrade vulnerable dependency** | **2 SP** | Security | Medium security risk. Low effort (2 SP), high compliance & risk prevention value. | **SELECTED** |
| **3** | **Payment retry bug fix** | **5 SP** | Customer / Financial | High customer impact. Direct financial transaction drop. | **SELECTED** |
| **7** | **Improve alert thresholds** | **3 SP** | Reliability / SRE | Prevents blind outages while error budget is near exhaustion. High reliability leverage. | **SELECTED** |
| **6** | Implement Feature A | 8 SP | Strategic Feature | Product priority, but 8 SP crowds out critical checkout & payment fixes during error budget crisis. | **DEFERRED** |
| **4** | Remove duplicate caching layer | 8 SP | Technical Debt | High technical debt, but low immediate customer impact. Defer to next sprint. | **DEFERRED** |
| **5** | Improve dashboard load time | 3 SP | Customer UX | Medium impact, non-critical internal admin tool. Defer. | **DEFERRED** |
| **8** | Add automated rollback validation | 5 SP | Operational Risk | High operational risk, but checkout/payment bugs take precedence. Manual rollback drill used as stopgap. | **DEFERRED** |
| **9** | Refactor deployment scripts | 5 SP | Productivity | Medium productivity impact. Defer. | **DEFERRED** |
| **10** | Add API usage analytics | 3 SP | Product Insight | Medium insight value. Defer. | **DEFERRED** |

---

## 🎯 Final Sprint Composition (Total: 15 Story Points)

```text
SELECTED WORK (15 / 16 SP Capacity):
  [5 SP] Fix Intermittent Checkout Timeout
  [5 SP] Fix Payment Retry Bug
  [3 SP] Improve Alert Thresholds
  [2 SP] Upgrade Vulnerable Dependency
```

---

## 💡 Trade-Off Defense & Stakeholder Communication

### 1. Defense to Product Leadership (Deferring Feature A - 8 SP):
> *"Feature A is highly valuable for business expansion. However, shipping Feature A into a service with an exhausted error budget and active checkout failures would exacerbate customer churn and cause Feature A transactions to fail. By allocating 15 SP to resolve checkout timeouts (400 tickets/wk) and payment retries now, we stabilize the platform so Feature A can launch safely in the very next sprint."*

### 2. Risk Acceptance:
- **Accepted Risk:** Deferring automated rollback validation (5 SP). **Mitigation:** Perform a manual two-person rollback verification script prior to deployments this sprint.
- **Accepted Risk:** Technical debt in duplicate caching layer remains for 1 additional sprint.

---

## 🚨 Mid-Sprint Incident Revision Strategy
> **Scenario:** On Day 4 of the sprint, a major SEV-1 production outage occurs.

**Action Plan:**
1. **Freeze Low-Priority Work:** Pause alert threshold fine-tuning (3 SP).
2. **Focus Capacity on Outage Resolution:** Re-allocate engineering bandwidth strictly to hot-fix resolution.
3. **Do NOT Pull Deferred Strategic Features:** Maintain freeze on Feature A (8 SP) during an active production incident. Re-plan sprint commitments formally after post-incident RCA.

---

## ✅ Self-Check & Completion Sign-Off
- [x] Evaluated full backlog across customer impact, business value, security, and technical debt.
- [x] Strictly enforced the 16 Story Point capacity limit (selected 15 SP).
- [x] Defended engineering trade-offs with data-driven evidence (support tickets, error budget health).
- [x] Formulated an actionable mid-sprint emergency response protocol.
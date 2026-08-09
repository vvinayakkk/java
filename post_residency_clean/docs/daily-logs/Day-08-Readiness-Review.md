# Guided Practice 8 – Engineering Readiness Review

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Artefact Reference:** [`docs/artefacts/day-08-release-evidence.md`](../artefacts/day-08-release-evidence.md)  
**Time Spent:** ~75 minutes (Production Readiness Review & Risk Assessment)

---

## 🏢 Engineering Scenario & Executive Summary
> "Tomorrow morning your engineering team plans to deploy 'Book Recommendations v1' to production. Development and QA signed off based on 98% test pass rates and successful load tests. Product leadership is pushing hard to launch on schedule. Your Tech Lead has asked YOU to perform the final Engineering Readiness Review and defend your decision during the Go/No-Go release meeting."

**Executive Summary & Release Decision:**
### Recommendation: **APPROVE WITH CONDITIONS**
Functional tests (98% pass) and performance load tests are green. However, four material operational risks—untested rollback procedures, missing business alert thresholds, a manual configuration step, and an unpatched medium CVE dependency vulnerability—pose significant operational risks that must be mitigated before routing live customer traffic.

---

## 📋 Facts vs. Assumptions vs. Unknowns Matrix

| Item / Category | Fact (Supported by Evidence) | Assumption (Needs Verification) | Unknown (Operational Gap) |
|---|---|---|---|
| **Test Results** | Automated unit/integration test pass rate is **98%**. | Assumed the remaining 2% test failures are non-critical edge cases. | Exact failure modes of the 2% failing tests under peak load. |
| **Performance** | Latency and throughput passed pre-release load testing. | Assumed load test dataset matches real production traffic distribution. | Database behavior under unexpected flash-sale traffic spikes. |
| **Rollback Plan** | Written rollback procedure document exists in repo. | Assumed rollback script will execute cleanly without schema locking. | **Rollback procedure has NEVER been tested in staging.** |
| **Observability** | Comprehensive application logging is enabled. | Assumed logs are sufficient to diagnose production outages. | **Monitoring lacks business metric alerts & SLI/SLO thresholds.** |
| **Security** | Medium-risk dependency vulnerability identified (awaiting vendor patch). | Assumed vulnerability cannot be exploited without authenticating. | Exploitability window before vendor releases security patch. |

---

## ⚠️ Risk Register & Mitigation Strategy

| Risk Description | Category | Likelihood | Impact | Priority | Recommended Mitigation |
|---|---|---|---|---|---|
| **Untested Rollback Procedure** | Operational | Medium | High | **HIGH** | Perform a mandatory live rollback drill in Staging environment today before deployment sign-off. |
| **Missing Business Alerts / SLIs** | Monitoring | High | High | **HIGH** | Configure Prometheus/Grafana alerts for 5xx error rate (>1%) and latency p95 (>500ms) prior to release. |
| **Manual Configuration Step** | Deployment | Medium | Medium | **MEDIUM** | Replace manual file edit with environment variable injection; require two-person verification if manual step remains. |
| **Unpatched CVE Vulnerability** | Security | Medium | Medium | **MEDIUM** | Log formal security risk exception with owner/target patch date; restrict exposed endpoints via Web Application Firewall (WAF). |

---

## 🚦 Release Decision & Mandatory Approval Gates

### Decision: **APPROVE WITH CONDITIONS**

#### Mandatory Conditions Required Before Opening Live Traffic:
1. **Rollback Drill Validation:** The engineering team must execute a successful dry-run rollback in Staging within <15 minutes.
2. **Alert Threshold Activation:** Minimum error-rate and p95 latency alerts must be active in PagerDuty/Grafana.
3. **Canary Staged Rollout:** Deploy using a 10% canary feature flag split; monitor error rates for 60 minutes before ramping up to 100% traffic.

---

## ✅ Self-Check & Completion Sign-Off
- [x] Separated verified facts from assumptions and unknown operational gaps.
- [x] Prioritized engineering risks based on likelihood, impact, and customer severity.
- [x] Formulated actionable, evidence-based mitigations for all High and Medium risks.
- [x] Defended a clear release recommendation (**Approve with Conditions**) suitable for a release review board.
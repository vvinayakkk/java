# Guided Practice 10 – Conduct an Effective Code Review

**Program:** Engineering Residency – From Training to Production Thinking  
**Date:** 2026-08-01  
**Engineer:** Vinayak  
**Artefact Reference:** [`docs/artefacts/day-10-pr-2481.md`](../artefacts/day-10-pr-2481.md)  
**Time Spent:** ~70 minutes (Pull Request Security & Code Quality Audit)

---

## 🏢 Engineering Scenario & Review Scope
> "You are assigned to perform the primary code review for Pull Request #2481: 'Add request-level caching to Product Search'. The PR author claims search latency dropped from 420ms to 170ms and all automated unit tests are passing. Your Tech Lead asks for a thorough production-readiness review before sign-off."

---

## 🔍 Code Snippet Severity Classification

| Snippet # | Code Excerpt / Observed Behavior | Severity Classification | Technical Engineering Rationale |
|---|---|---|---|
| **Snippet C** | `String sql = "SELECT * FROM products WHERE id=" + id;` | **BLOCKER** | **SQL Injection Vulnerability.** Direct string concatenation allows arbitrary SQL command execution. Must use parameterized queries (`PreparedStatement` or JPA Repository methods). |
| **Snippet B** | `log.info("User {} searched {}", userId, query);` | **SHOULD FIX** | **PII & Privacy Leakage.** Logging raw user IDs alongside search queries violates privacy standards (GDPR/HIPAA). Query parameters should be sanitized or debug-logged without user association. |
| **Snippet E** | New cache implementation lacks eviction policy / TTL. | **SHOULD FIX** | **Memory Leak / OOM Risk.** Unbounded caching without eviction strategy causes heap memory inflation and eventual JVM Out-Of-Memory crashes under high query cardinality. |
| **Snippet A** | `cache.put(query, result);` | **SHOULD FIX** | Unbounded key cardinality. High permutations of search strings will saturate memory. |
| **Snippet F** | Two critical edge cases missing in unit tests. | **SHOULD FIX** | Inadequate test coverage for null search queries and empty result sets. |
| **Snippet G** | Nested loop (`O(N^2)`) executes on every search request. | **SHOULD FIX** | CPU latency bottleneck. Will cause CPU spikes as catalog dataset size increases. |
| **Snippet D** | Duplicated validation method copied from another service. | **NICE TO HAVE** | Violates DRY principle. Should refactor into a shared validation utility class. |

---

## 💬 Constructive Code Review Comments

### Comment on Snippet C (Blocker - Security):
> **Line 45 (SearchService.java):**  
> ⚠️ **[BLOCKER - Security]** Constructing SQL queries via string concatenation (`"SELECT * FROM products WHERE id=" + id`) introduces a critical SQL Injection vulnerability.  
> **Recommendation:** Please refactor this query to use Spring Data JPA repository method handles (e.g., `productRepository.findById(id)`) or parameterized HQL/NamedParameters:
> ```java
> @Query("SELECT p FROM Product p WHERE p.id = :id")
> Optional<Product> findByIdParam(@Param("id") Long id);
> ```

### Comment on Snippet E (Should Fix - Reliability):
> **Line 22 (CacheManager.java):**  
> ⚠️ **[SHOULD FIX - Reliability]** The cache map does not define an eviction policy or maximum size bound. Under high search traffic, storing arbitrary query strings will cause heap memory saturation and eventual JVM Out-Of-Memory errors.  
> **Recommendation:** Integrate Caffeine or Spring Cache with explicit TTL (`expireAfterWrite=60s`) and bounded capacity (`maximumSize=1000`).

---

## 💬 Response to Existing Reviewer Comments

- **Reviewer A ("Looks good to me"):** **Disagree.** The review missed a critical SQL Injection blocker (Snippet C) and memory leakage risks. LGTM approval should be revoked until security issues are addressed.
- **Reviewer B ("We should use Redis instead"):** **Partially Disagree as a mandatory blocker.** Redis is ideal for distributed multi-instance caching, but an in-memory Caffeine cache is acceptable for single-instance search if properly bounded with TTL and eviction.
- **Reviewer C ("Concerned about stale cache entries"):** **Agree.** Unbounded caching without invalidation or TTL guarantees stale data displays.

---

## 🚦 Overall PR Recommendation

### Recommendation: **REQUEST CHANGES**
While the 420ms → 170ms latency reduction is impressive, PR #2481 cannot be merged due to a critical **SQL Injection blocker** (Snippet C) and **unbounded memory leakage risks** (Snippet E).

---

## ✅ Self-Check & Completion Sign-Off
- [x] Evaluated all 7 code snippets and classified severity (Blockers vs Should Fix vs Nits).
- [x] Evaluated existing reviewer comments objectively using engineering principles.
- [x] Formulated constructive, professional code review feedback with code examples.
- [x] Made a defensible merge recommendation (**Request Changes**) prioritizing security and system stability.
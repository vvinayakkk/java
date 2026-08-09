# Paste this into Cursor after Java + Postman are installed

Copy everything inside the fenced block below into a **new chat**.

---

```text
You are continuing my Engineering Residency pack in:

/Users/vinayak.b/Desktop/post_bootcamp

## Program documentation requirement (mandatory)
The residency requires ONE continuous practice document for all Guided Practices (ask.md: Google Doc).
In this pack that document is:

  docs/practice-log.md

You MUST maintain it as you work:
- Keep the shared section shape: Context / Evidence / Work / Engineering Judgment / Outcome / Recommendation / Self-check
- Fill every field the program asks for each day (see each docs/day-XX-*.md “What to record”)
- Use real class names, endpoints, timings (ms), and evidence — not placeholders
- Tick self-check boxes only after the evidence is actually written
- Do NOT create a second competing log; update practice-log.md in place
- Optionally note at the top if content was copied into a Google Doc for official submission

Also keep these docs accurate if live results change assumptions:
- docs/READY-FOR-JAVA.md (mark steps complete)
- docs/00-program-overview.md status line if needed
- Do not rewrite day guides unless a step is wrong vs the running app

## Context (already done — do NOT redo from scratch)
- Repo: spring-bookstore/ (clone of shafakyildiz/spring-bookstore)
- Day 0: DataLoader seeds ~90 books; CatalogSyncService hook exists
- Day 3: Pagination + sorting on GET /api/books → BookPageResponse (coded)
- Day 5: Caffeine cache on BookService.getBookById + CacheEvict on writes (coded)
- Day 6: catalog sync supports blocking vs @Async via properties (coded)
- docs/practice-log.md: GP1–3 narrative + GP5–12 reports drafted; GP4 timings EMPTY; GP3/5/6 live verify + numbers still pending
- Checklist: docs/READY-FOR-JAVA.md
- Original brief: ask.md

## Your job NOW (live verify + finish the practice doc)
1. Verify JDK 17+ and Maven: `java -version`, `mvn -version`
2. In spring-bookstore/: `mvn clean test` — fix failures if any; note results in a short “Verification” note at the top of practice-log.md
3. Start app: `mvn spring-boot:run` (confirm seed log)
4. Smoke-test:
   - GET /api/books?page=0&size=5&sortBy=title&sortDir=asc
   - GET /api/books/1
   - GET /api/books/search?title=Patterns
   Update GP3 Evidence (testing performed) + tick Postman/existing-functionality self-checks
5. Day 4 — measure 5 runs each (1 warmup discarded). Fill GP4 fully per ask.md record fields:
   endpoints, individual times, averages, slowest, bottleneck, evidence, next investigation
   Endpoints:
   - GET /api/books/1
   - GET /api/books?page=0&size=10
   - GET /api/books/search?title=Patterns
6. Day 5 — measure cache miss vs warm hits on GET /api/books/1; verify eviction after PUT; fill GP5 before/after + tick measurement self-check. Keep production recommendation.
7. Day 6 — measure POST /api/books:
   A) enabled=true, delay-ms=2000, async=false → restart → 5 unique ISBN creates
   B) async=true → restart → 5 new ISBN creates
   Fill GP6 before/after, confirm diagrams still match reality, tick measurement self-check
   Restore: enabled=false, delay-ms=0, async=true
8. Doc hygiene pass on practice-log.md:
   - No “TBD” / empty timing cells left for GP4–6
   - All self-checks for GP3–6 ticked or honestly left unticked with reason
   - GP1–2: add one line that live GET was confirmed after install (if true)
   - GP7–12: leave as-is unless a factual conflict with the running system appears
9. Mark docs/READY-FOR-JAVA.md Steps 1–6 complete
10. Reply with: test status, timing tables, confirmation that practice-log.md is submission-ready

## Rules
- Documentation is part of the deliverable, not optional cleanup
- Do not remove intentional code smells (EAGER fetch, field injection) unless I ask
- Prefer curl if Postman CLI unavailable; record times in ms
- Keep code changes minimal — only fix breakages found while verifying
- Match ask.md “How to Record” fields for each Guided Practice

Start by checking java/mvn, then run tests, then update practice-log.md as you go (not only at the end).
```

---

When this finishes, `docs/practice-log.md` should be the complete submission-style practice document (the program’s Google Doc equivalent), with real timings filled in.

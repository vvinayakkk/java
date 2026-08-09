					
	Program	Engineering Residency – From Training to Production Thinking			
	Duration	12 Working Days			
	Daily Learning Flow	Learn (Video/Article) : 30–40 mins			
		Build (Hands-on Exercise) : 45–60 mins			
		AI Review (Cursor) : 10–15 mins			
		Reflection : 10 mins			
	Daily Time	1.5–2 Hours			
	Total Learning	~25 Hours			
					
	Unit	Unit 1 – Think Like an Engineer			
	Guided Practice	Reading an Existing Codebase			
	Estimated Time	2 Hours			
	🏢 Engineering Scenario				
	"You've just joined a new engineering team. Before making any code changes, your first responsibility is to understand how the existing application is structured. 
In this Guided Practice, you'll explore a real Spring Boot project, trace how requests flow through the application, and begin thinking like an engineer responsible for maintaining production software."				
	🎯 What should I learn?				
	"By the end of this Guided Practice, you should be able to:
- Understand how a typical Spring Boot backend project is organized.
- Explain the responsibility of Controllers, Services, Repositories, and Models.
- Trace an HTTP request from the API layer to the database.
- Validate your understanding of unfamiliar code using AI."				
	📚 Learning Path				
	Priority	Resource	Duration	Focus	
	✅ Mandatory	"Spring Guide – Building a RESTful Web Service
 https://spring.io/guides/gs/rest-service"	0.33	Understand what a Spring Boot application looks like.	
	✅ Mandatory	"Spring Boot Code Structure: Package by Layer vs Package by Feature
 https://www.youtube.com/watch?v=B1d95I7-zsw"	0.33	Learn why backend projects are organized into layers.	
	📖 Good to Know	"GeeksforGeeks – Spring Boot Code Structure
 https://www.geeksforgeeks.org/java/spring-boot-code-structure/"	0.25	Reinforce the responsibility of each package and layer.	
	💡 Optional / Refresher	"Cursor Learn – Understanding Your Codebase
 https://cursor.com/learn/understanding-your-codebase"	0.17	Learn AI-assisted code exploration.	
	💻 Mandatory Practice Exercise				
	"Using a small Spring Boot CRUD project from GitHub:
 1. Locate the controller package.
 2. Locate the service package.
 3. Locate the repository package.
 4. Locate the model/entity package.
 5. Find one GET endpoint.
 6. Trace the request flow: Client → Controller → Service → Repository → Database.
 7. Identify where the business logic lives. 
 8. Why do you think the business logic belongs in this layer instead of the Controller?"				
	📤 How to Record Your Practice Exercise				
	"Create one Google Doc to record your Mandatory Practice Exercises throughout the Post-Training Program. Use the same document for all Guided Practices.
 
For this exercise, add a section titled Guided Practice 1 – Reading an Existing Codebase and record:
 • GitHub Repository: Paste the link to the project you explored.
• Controller: Package/file name you identified.
• Service: Package/file name you identified.
• Repository: Package/file name you identified.
• Model/Entity: Package/file name you identified.
• GET Endpoint: The endpoint you traced.
• Request Flow: Show the flow using the actual class and method names: Controller → Service → Repository → Database.
• Business Logic: In 1–2 sentences, identify where the business logic is located and briefly explain what it does."				
	🤖 AI Companion (Optional)				
	"Open the project in Cursor and ask:
 • Explain this project architecture.
 • Trace the GET endpoint from request to database.
 • Which design pattern is this project using?
 Compare the answers with the actual code."				
	✅ How do I know I'm done?				
	"Mark this Guided Practice as COMPLETE on the Completion Status Tab once you have:
 ☐ Completed all Mandatory learning resources.
 ☐ Completed the Mandatory Practice Exercise.
 
 Self Check:
 ☐ I can explain the project structure.
 ☐ I can identify the Controller, Service and Repository layers.
 ☐ I can trace one API request.
 ☐ I know where business logic lives."				
	🚀 Take it Further (Optional)				
	"• Explore another endpoint.
• Compare with another Spring Boot project.
• Read about Layered Architecture and Dependency Injection."				
					
	Unit	Unit 2 – Debug Like an Engineer			
	Guided Practice	Investigating & Improving Existing Code			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Trace how a request flows through an existing Spring Boot application.
• Investigate the behaviour of an existing feature.
• Identify maintainability issues using recognised engineering practices.
• Explain why an issue affects code quality.
• Recommend practical improvements without changing the implementation.
• Develop a production engineer's approach to code investigation."				
	📚 Learning Path				
	Priority	Resource	Duration	Focus	
	✅ Mandatory	"Martin Fowler – Code Smells
https://martinfowler.com/bliki/CodeSmell.html"	20 mins	Recognising maintainability issues	
	✅ Mandatory	"Refactoring Guru – Code Smells
https://refactoring.guru/refactoring/smells"	25 mins	Common engineering issues	
	📖 Good to Know	"Google Engineering Practices
https://google.github.io/eng-practices/"	20 mins	Engineering decision making	
	💡 Optional	"Refactoring Guru – Refactoring Catalog
https://refactoring.guru/refactoring/catalog"	20 mins	Improvement techniques	
	💻 Mandatory Practice Exercise				
	"Using the same Spring Boot project from Unit 1:
1. Select one endpoint.
2. Execute it using Postman.
3. Trace the flow: Client → Controller → Service → Repository → Database.
4. Identify ONE code smell or maintainability issue.
5. Explain why it is a problem.
6. Recommend a practical improvement.
7. Explain the expected engineering benefit.

Do NOT modify the code."				
	📤 How to Record Your Practice Exercise				
	"Add a new section to your Google Doc.

Record:
• Repository
• Endpoint investigated
• Request flow 
• Code smell identified
• Why it matters
• Recommended improvement
• Expected engineering impact"				
	🤖 AI Companion (Optional)				
	"Use your preferred AI assistant to:
• Explain the request flow.
• Identify possible code smells.
• Review your analysis
• Suggest improvements

Validate every AI suggestion before accepting it."				
	✅ How do I know I'm done?				
	"☐ Completed the Mandatory learning.
☐ Completed the Practice Exercise.
☐ Updated the Google Doc.

Self Check
☐ I can trace the request flow confidently.
☐ I can recognise common code smells.
☐ I can justify an engineering improvement."				
	🚀 Take it Further (Optional)				
	Investigate a second endpoint and compare whether the same maintainability issues appear elsewhere in the application. Identify the engineering practice that could address them.				
					
	Unit	Unit 3 – Deliver Features Like an Engineer			
	Guided Practice	Implementing a Small Feature in an Existing Codebase			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Interpret a small feature request.
• Identify the correct classes to modify.
• Implement a safe, incremental change in an existing codebase.
• Verify that existing functionality continues to work.
• Explain the engineering decisions and trade-offs behind your implementation.
• Deliver a feature with production engineering discipline."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Google Engineering Practices – Code Review Best Practices
https://google.github.io/eng-practices/review/"	20 mins	Learn how to make safe, reviewable code changes.	
	✅ Mandatory	"Martin Fowler – YAGNI
https://martinfowler.com/bliki/Yagni.html"	10 mins	Avoid unnecessary complexity and over-engineering.	
	📖 Good to Know	"Spring Boot Guides (Reference Only)
https://spring.io/guides"	20 mins	Reference official Spring Boot implementation examples when building your feature.	
	💡 Optional	"Google Testing Blog
https://testing.googleblog.com/"	20 mins	Learn real-world testing and software quality practices from Google's engineering teams.	
	💻 Mandatory Practice Exercise				
	"Continue using the same Spring Boot project from Units 1 and 2.

Implement ONE enhancement:
• Input validation
• Filtering
• Sorting
• Improved error handling

1. Understand the requirement.
2. Identify affected classes.
3. Implement the enhancement.
4. Test using Postman.
5. Verify existing functionality.
6. Record your engineering decisions.

Focus on making the smallest safe change."				
	📤 How to Record Your Practice Exercise				
	"Update your Google Doc with:
• Feature implemented
• Classes modified
• Why those classes were chosen
• Testing performed
• Issues encountered
• Engineering trade-offs
• One future improvement"				
	🤖 AI Companion (Optional)				
	"Optionally use AI to:
 • Review your implementation.
 • Suggest edge cases.
 • Suggest additional tests.
 Review every suggestion before using it."				
	✅ How do I know I'm done?				
	"☐ Mandatory learning completed
☐ Enhancement implemented
☐ Tested with Postman
☐ Existing functionality verified
☐ Google Doc updated

Self Check
☐ I can justify every code change.
☐ I delivered the smallest safe implementation."				
	🚀 Take it Further (Optional)				
	Add automated tests for your enhancement or implement a second enhancement while maintaining backward compatibility.				
					
	Unit	Unit 4 – Measure Performance Like an Engineer			
	Guided Practice	Measuring API Performance			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Explain why performance should be measured before it is optimized.
• Measure the response time of an API.
• Compare the performance of different endpoints.
• Identify potential performance bottlenecks using evidence.
• Document your findings and recommend where further investigation is needed."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Focus	
	✅ Mandatory	"Google Web Fundamentals – Measuring Performance
https://web.dev/performance/?utm_source=chatgpt.com"	20 mins	Understand why performance measurement matters.	
	✅ Mandatory	"Postman Performance / Response Time Basics
https://learning.postman.com/docs/use/send-requests/response-data/responses?utm_source=chatgpt.com"	15 mins	Measure response times consistently.	
	📖 Good to Know	"Martin Fowler – Performance
https://martinfowler.com/articles/is-quality-worth-cost.html?utm_source=chatgpt.com"	15 mins	Engineering trade-offs around optimisation.	
	💡 Optional	"Engineering case study (Stripe/Uber/Netflix)
https://netflixtechblog.com/?utm_source=chatgpt.com"	20 mins	Learn how engineering teams investigate performance.	
	💻 Mandatory Practice Exercise				
	"Continue using the same Spring Boot project.

Choose THREE API endpoints.
1. Execute each endpoint five times.
2. Record the response time for every request.
3. Calculate the average response time.
4. Compare the results.
5. Identify the slowest endpoint.
6. Suggest one possible reason why it might be slower.
7. Explain what additional information you would need before making any optimisation.

Do NOT modify the application.
The goal is to investigate—not optimise."				
	📤 How to Record Your Practice Exercise				
	"Update your Google Doc with:
• Endpoints tested
• Individual response times
• Average response time
• Slowest endpoint
• Possible bottleneck
• Evidence supporting your conclusion
• What you would investigate next"				
	🤖 AI Companion (Optional)				
	"Optionally use AI to:
• Review your measurements.
• Suggest possible causes for the observed differences.
• Recommend additional measurements.

Review every suggestion before using it."				
	✅ How do I know I'm done?				
	"☐ Mandatory learning completed
☐ Three endpoints measured
☐ Average response times calculated
☐ Findings documented
☐ Google Doc updated

Self Check
☐ I can explain why measuring comes before optimisation.
☐ I can compare API performance using evidence.
☐ I can justify where I would investigate further."				
	🚀 Take it Further (Optional)				
	Measure the same endpoints after making a small change (for example, enabling additional logging or changing the dataset size) and compare the results. Document whether the change had a measurable impact.
				
					
	Unit	Unit 5 – Cache with Purpose 			
	Guided Practice	Designing & Implementing a Production Caching Strategy			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Decide whether caching is the right solution for a performance problem.
• Select an appropriate caching approach for a Spring Boot service.
• Justify cache keys, TTLs and invalidation strategy using engineering reasoning.
• Measure the impact of caching using evidence.
• Recommend whether the solution is production-ready."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Spring Framework – Cache Abstraction (Read all 7 sub-topics)
https://docs.spring.io/spring-framework/reference/integration/cache.html"	20 mins	Understand Spring's cache abstraction and annotations.	
	✅ Mandatory	"Spring Boot – Caching
https://docs.spring.io/spring-boot/reference/io/caching.html"	20 mins	Enable caching in a Spring Boot application.	
	📖 Good to Know	"Cache-Aside Pattern
https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside?utm_source=chatgpt.com"	15 mins	Choosing the right caching strategy and understanding consistency trade-offs.	
	📖 Good to Know	"Cloudflare Learning Center – What is Caching?
https://www.cloudflare.com/learning/cdn/what-is-caching/"	15 mins	Thinking beyond application caches.	
	💡 Optional	"High Scalability
https://highscalability.com/"	15 mins	Read one production engineering article involving caching or performance.	
	💻 Mandatory Practice Exercise				
	"In Unit 4, you identified the slowest endpoint in your Spring Boot application. Your Tech Lead has asked you to investigate whether caching is the right solution before any optimisation is approved.

Your Task: Using the same Spring Boot application, investigate whether caching is appropriate for the identified endpoint.
Your recommendation should be based on engineering evidence, rather than assumptions.

As part of your investigation:
1. Decide whether caching is appropriate.
2. Choose the most suitable approach (No Cache, Local Cache or Distributed Cache) and justify your decision.
3. Define your cache strategy, including the cache key, TTL and invalidation approach.
4. Implement the solution if appropriate.
5. Measure the endpoint before and after your changes.
6. Identify at least one benefit and one trade-off introduced by your solution.
7. Recommend whether you would approve this implementation for production, and explain why."				
	📤 How to Record Your Practice Exercise				
	"Update your Google Doc with:
• Endpoint investigated
• Evidence collected
• Cache decision
• Cache design
• Cache key
• TTL
• Invalidation strategy
• Before/after response times
• Engineering trade-offs
• Final production recommendation"				
	🤖 AI Companion (Optional)				
	"Optionally use AI to:
• Review your cache strategy.
• Challenge your engineering assumptions.
• Suggest edge cases you may have missed.

Review every suggestion before using it."				
	✅ How do I know I'm done?				
	"☐ Mandatory learning completed
☐ Investigation completed
☐ Design justified with evidence
☐ Implementation completed (if appropriate)
☐ Before/after measurements recorded
☐ Production recommendation documented

Self Check

☐ I can explain why caching is or is not the correct optimisation.
☐ I can defend my design decisions during a code review."				
	🚀 Take it Further (Optional)				
	Investigate a second endpoint and decide whether a different caching strategy—or no caching at all—is more appropriate. Compare your recommendations and explain the trade-offs.				
					
	Unit	Unit 6 – Redesign a Production Workflow			
	Guided Practice	Improving User Experience Through Workflow Redesign			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Analyse how a user request flows through a production system.
• Identify work that unnecessarily delays the user.
• Distinguish between work that must complete immediately and work that can safely be deferred.
• Redesign the workflow to improve responsiveness while preserving correctness and reliability.
• Justify every design decision using engineering evidence."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Martin Fowler – Patterns of Event-Driven Architecture
 https://martinfowler.com/articles/201701-event-driven.html"	20 mins	Understand workflow design and responsiveness.	
	✅ Mandatory	"Confluent Developer – Event-Driven Design
 https://developer.confluent.io/"	20 mins	Learn how production systems redesign long-running workflows.	
	📖 Good to Know	"Spring for Apache Kafka Reference
 https://docs.spring.io/spring-kafka/reference/"	15 mins	Reference only if implementation requires it.	
	📖 Good to Know	"Apache Kafka Documentation
 https://kafka.apache.org/documentation/"	15 mins	Refresh Bootcamp concepts only when needed.	
	💡 Optional	"High Scalability
 https://highscalability.com/"	15 mins	Read a production workflow case study.	
	💻 Mandatory Practice Exercise				
	"Engineering Scenario: Your team recently completed a performance improvement initiative. API latency has improved and caching has reduced response times. Despite these improvements, users still experience delays because multiple operations execute before the response is returned.

Your Tech Lead has asked you to investigate and redesign the workflow.

Tasks:
1. Map the current request lifecycle.
2. Identify user-blocking activities.
3. Decide which activities must occur before the response and which can safely occur afterwards.
4. Redesign the workflow. Your solution may include asynchronous processing, background jobs, batching, scheduled execution or another approach.
5. Implement ONE improvement.
6. Measure before/after response times.
7. Evaluate benefits, trade-offs and risks.
8. Recommend whether the redesign is production ready."				
	📤 How to Record Your Practice Exercise				
	"Update your Google Doc with:
• Current workflow diagram
• Redesigned workflow diagram
• User-blocking activities
• Design decisions and rationale
• Alternatives considered
• Before/after measurements
• Risks and failure scenarios
• Final production recommendation"				
	🤖 AI Companion (Optional)				
	"Optionally use AI to:
• Critique your workflow redesign 
• Identify missing failure scenarios
• Challenge your assumptions 
• Suggest alternatives. 

Validate every recommendation before adopting it."				
	✅ How do I know I'm done?				
	"☐ Mandatory learning completed
☐ Existing workflow analysed
☐ Redesigned workflow documented
☐ Engineering decisions justified
☐ One improvement implemented
☐ Measurements recorded
☐ Risks evaluated
☐ Production recommendation completed

Self Check

☐ I can explain why my redesign improves the user experience.
☐ I can defend my design decisions during an architecture review.
☐ I understand why I chose this solution instead of another."				
	🚀 Take it Further (Optional)				
	Choose another workflow in your application. Repeat the same investigation and compare your redesign decisions.				
					
	Unit	Unit 7 – Investigate a Production Incident			
	Guided Practice	Performing Root Cause Analysis for a Production System			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Investigate a production issue using a structured engineering approach.
• Distinguish symptoms from root causes.
• Gather and interpret evidence from logs, metrics and system behaviour.
• Evaluate multiple hypotheses before reaching a conclusion.
• Recommend an evidence-based remediation plan suitable for production."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Google SRE Workbook – Chapter 9: Incident Response
https://sre.google/workbook/incident-response/"	20 mins	Learn a structured, evidence-based approach to diagnosing production issues.	
	✅ Mandatory	"Google SRE Book – Chapter 12: Effective Troubleshooting
https://sre.google/sre-book/effective-troubleshooting/"	15 mins	Understand how engineering teams investigate, manage and communicate during production incidents.	
	📖 Good to Know	"Spring Boot Actuator Documentation
https://docs.spring.io/spring-boot/reference/actuator/index.html?utm_source=chatgpt.com"	15 mins	Learn how to use runtime diagnostics to investigate application behaviour.	
	📖 Good to Know	"OpenTelemetry Concepts (Overview)
https://opentelemetry.io/docs/concepts/?utm_source=chatgpt.com"	15 mins	Understand how logs, metrics and traces work together during production investigations.	
	💡 Optional	"Google SRE Book – Monitoring Distributed Systems
https://sre.google/sre-book/managing-incidents/?utm_source=chatgpt.com"	20 mins	Explore production incident management and post-incident best practices.	
	💻 Mandatory Practice Exercise				
	"Engineering Scenario: Over the past 24 hours, customer complaints have increased. Users report slow requests and occasional failures following the latest deployment. Dashboards confirm increased response times, but no root cause has been identified.

Your Tech Lead has asked you NOT to implement a fix immediately. Determine what is happening before proposing a solution.

Tasks:
1. Understand the incident.
2. Gather evidence from request flow, logs, metrics, database interactions, external services, cache behaviour, background processing and recent code changes.
3. Develop at least three hypotheses.
4. Evaluate evidence supporting and contradicting each hypothesis until you identify the most likely root cause.
5. Prepare a production recommendation with the root cause, evidence, remediation, risks and validation required before deployment."				
	📤 How to Record Your Practice Exercise				
	"Prepare an Incident Investigation Report containing:
• Incident summary
• Customer & business impact
• Investigation timeline
• Evidence collected
• Hypotheses considered
• Root cause analysis
• Recommended remediation
• Risks
• Follow-up actions"				
	🤖 AI Companion (Optional)				
	"Optionally use AI to:
• Critique your investigation process.
• Suggest additional hypotheses.
• Identify missing evidence.
• Challenge your conclusions.
• Review your remediation plan.

Validate every recommendation before adopting it."				
	✅ How do I know I'm done?				
	"☐ Mandatory learning completed
☐ Incident understood
☐ Evidence collected
☐ Multiple hypotheses evaluated
☐ Root cause identified
☐ Recommendation supported by evidence
☐ Incident Investigation Report completed

Self Check
☐ I can distinguish symptoms from root causes.
☐ I justify conclusions using evidence.
☐ I investigate before proposing solutions.
☐ I can confidently explain my findings during an incident review."				
	🚀 Take it Further (Optional)				
	Investigate a different production issue (e.g. increased error rates instead of latency). Compare your investigation process, evidence collected and conclusions.				
					
	Unit	Unit 8 – Conduct an Engineering Readiness Review			
	Guided Practice	Assessing Production Readiness Before Deployment			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
 • Evaluate production risk using engineering evidence.
 • Distinguish feature completeness from operational readiness.
 • Prioritize engineering risks based on customer and business impact.
 • Recommend whether to Approve, Approve with Conditions or Reject a production release.
 • Defend your recommendation during an engineering review."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Google SRE Workbook – Reliable Product Launches
https://sre.google/resources/book-update/reliable-product-launches-at-scale/"	20 mins	Learn how engineering teams evaluate whether a release is ready for production and reduce deployment risk.	
	✅ Mandatory	"Google SRE Book – Release Engineering
https://sre.google/sre-book/release-engineering/"	20 mins	Understand release pipelines, deployment automation, staged rollouts and safe production releases.	
	📖 Good to Know	"Martin Fowler – Feature Toggles
https://martinfowler.com/articles/feature-toggles.html"	20 mins	Learn how feature flags reduce deployment risk, enable canary releases and support gradual rollouts.	
	📖 Good to Know	"Spring Boot Actuator Documentation
https://docs.spring.io/spring-boot/reference/actuator/index.html"	15 mins	Learn how health endpoints, metrics and runtime diagnostics help validate production readiness.	
	💡 Optional	"Google SRE Workbook – Configuration Design
https://sre.google/workbook/configuration-design/"	20 mins	Understand how configuration management and deployment practices improve production safety and reduce operational risk.	
	💻 Mandatory Practice Exercise				
	"Engineering Scenario: Tomorrow morning your team plans to deploy a new feature to production.
Development and QA have signed off. Product wants to release on schedule because the launch supports an important customer commitment.
Your Tech Lead has asked YOU to perform the final Engineering Readiness Review.
Your recommendation will be presented during the release approval meeting.

Information Available:
✓ Performance testing passed
✓ Load testing passed
✓ Automated tests: 98% pass rate
✓ Comprehensive application logging

⚠ Monitoring lacks business metrics and alert thresholds.
⚠ Rollback procedure exists but has never been tested.
⚠ One deployment configuration still requires manual editing.
⚠ A medium-risk dependency vulnerability is awaiting a vendor patch.

Your Tasks:
Phase 1 – Review the Evidence
• Separate facts, assumptions and unknowns.
Phase 2 – Identify Risks
• Identify customer, operational, deployment and business risks.
• Estimate likelihood, impact and priority.
Phase 3 – Recommend Mitigations
• Recommend mitigations for Medium and High risks.
Phase 4 – Make the Release Decision
Choose ONE:
• Approve
• Approve with Conditions
• Reject
Support every decision with engineering evidence.
Phase 5 – Prepare for the Release Review
Summarise your recommendation and explain what evidence influenced your decision most."				
	📤 How to Record Your Practice Exercise				
	"Create an Engineering Readiness Review containing:
• Executive Summary
• Evidence Reviewed
• Facts vs Assumptions
• Risk Register
• Recommended Mitigations
• Conditions for Approval
• Rollback Readiness
• Deployment Recommendation
• Outstanding Follow-up Actions"				
	🤖 AI Companion (Optional)				
	"Optionally use AI to:
• Act as a skeptical Tech Lead reviewing your recommendation.
• Challenge your assumptions.
• Argue the opposite deployment decision.
• Identify operational risks you may have overlooked.
• Review the strength of your evidence.

Validate every recommendation before adopting it."				
	✅ How do I know I'm done?				
	"☐ Mandatory learning completed
☐ Evidence reviewed
☐ Risks prioritised
☐ Mitigations recommended
☐ Deployment recommendation justified
☐ Engineering Readiness Review completed

Self Check

☐ I can distinguish facts from assumptions.
☐ I can justify risk using engineering evidence.
☐ I can defend my recommendation during a release review.
☐ I understand why reasonable engineers may reach different conclusions."				
	🚀 Take it Further (Optional)				
	Repeat the review for a second feature (e.g. an internal admin tool versus a customer-facing payment feature). Compare the different risks you would accept and explain why.				
					
	Unit	Unit 9 – Prioritise Engineering Work			
	Guided Practice	Prioritizing Engineering Initiatives			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
 • Evaluate engineering work using customer, business and operational impact.
 • Balance feature delivery, reliability, security and technical debt.
 • Prioritise competing work within limited engineering capacity.
 • Defend engineering trade-offs using evidence.
 • Produce a realistic Sprint Prioritisation Proposal."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Google SRE Workbook – Addressing Toil
https://sre.google/workbook/eliminating-toil/?utm_source=chatgpt.com"	20 mins	Learn how engineering teams prioritise work that delivers long-term value.	
	✅ Mandatory	"Google SRE Book – Eliminating Toil
https://sre.google/sre-book/eliminating-toil/?utm_source=chatgpt.com"	20 mins	Understand why engineering time is a limited resource.	
	📖 Good to Know	"Google SRE Workbook – Error Budgets
https://sre.google/workbook/error-budget-policy/?utm_source=chatgpt.com"	15 mins	Learn how reliability affects engineering priorities.	
	📖 Good to Know	"Engineering blog on Technical Debt
https://martinfowler.com/bliki/TechnicalDebtQuadrant.html?utm_source=chatgpt.com"	15 mins	See how successful teams balance competing priorities.	
	💻 Mandatory Practice Exercise				
	"Engineering Scenario:  You inherit a production service with the following backlog.
Engineering Capacity:
 • Maximum 16 Story Points this sprint.
  Stakeholder Context:
 • Product: A key customer is waiting for Feature A.
 • Support: Checkout timeout generates 400 tickets/week.
 • Security: Dependency vulnerability should be patched this sprint.
 • SRE: Error budget is nearly exhausted.
 
Current Backlog
  1. Fix intermittent checkout timeout (5 SP)
  Customer Impact: Very High | Business Value: Very High
  2. Upgrade vulnerable dependency (2 SP)
  Security Risk: Medium
  3. Add automated rollback validation (5 SP)
  Operational Risk: High if omitted
  4. Remove duplicate caching layer (8 SP)
  Technical Debt: High | Customer Impact: Low
  5. Improve dashboard load time (3 SP)
  Customer Impact: Medium
  6. Implement Feature A (8 SP)
  Business Value: Very High
  7. Improve alert thresholds (3 SP)
  Reliability Impact: High
  8. Payment retry bug (5 SP)
  Customer Impact: High
  9. Refactor deployment scripts (5 SP)
  Engineering Productivity: Medium
  10. Add API usage analytics (3 SP)
  Product Insight: Medium
  There is NO perfect sprint.
 
 Your Tasks
  Phase 1 – Understand the Backlog
 • Identify dependencies and urgent work.
  Phase 2 – Evaluate Every Item
 • Consider customer impact, business value, engineering effort, operational risk and technical debt.
  Phase 3 – Build the Sprint
 • Select work worth no more than 16 Story Points.
 • Explain why every selected item made the cut.
 • Explain why every deferred item was postponed.
  Phase 4 – Defend Your Decisions
 • Describe the trade-offs.
 • Explain how different stakeholders may disagree.
  Phase 5 – Mid-Sprint Change
 A major production incident occurs on Day 4.
 Revisit your sprint plan and explain what changes."				
	📤 How to Record Your Practice Exercise				
	"Create a Sprint Prioritisation Proposal containing:
 • Executive Summary
 • Prioritisation Criteria
 • Backlog Assessment
 • Selected Sprint Work
 • Deferred Work
 • Trade-off Analysis
 • Stakeholder Impact
 • Risks Accepted
 • Success Measures"				
	🤖 AI Companion (Optional)				
	"Optionally use AI to:
 • Act as an Engineering Manager reviewing your sprint plan.
 • Argue for a different prioritisation.
 • Identify hidden dependencies.
 • Highlight undervalued work items.
 • Explain how different stakeholders may challenge your proposal.
 
 Validate every recommendation before adopting it."				
	✅ How do I know I'm done?				
	" ☐ Mandatory learning completed
 ☐ Entire backlog evaluated
 ☐ Sprint fits within 16 Story Points
 ☐ Trade-offs justified
 ☐ Stakeholder impact considered
 ☐ Sprint Prioritisation Proposal completed
 
 Self Check
 
 ☐ I can explain why some valuable work must sometimes wait.
 ☐ I can defend prioritisation decisions using evidence.
 ☐ I understand that engineering prioritisation is about making informed trade-offs, not finding perfect answers."				
	🚀 Take it Further (Optional)				
	Repeat the exercise assuming the business has doubled the engineering capacity to 32 Story Points. Compare your new sprint plan and explain what changed—and why.				
					
	Unit	Unit 10 – Conduct an Effective Engineering Code Review			
	Guided Practice	Reviewing Code for Production Readiness			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
 • Evaluate production code beyond correctness.
 • Distinguish blockers from improvements.
 • Balance security, performance, maintainability and delivery.
 • Write constructive review comments.
 • Produce a professional Pull Request Review Report."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Google Engineering Practices – Code Review
https://google.github.io/eng-practices/review/?utm_source=chatgpt.com"	20 mins	Learn how Google engineers perform effective code reviews.	
	✅ Mandatory	"Google Engineering Practices – Writing Good CLs
https://google.github.io/eng-practices/review/developer/?utm_source=chatgpt.com"	20 mins	Understand what makes a change reviewable.	
	📖 Good to Know	"OWASP Secure Coding Practices
https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/"	15 mins	Recognise common security issues.	
	📖 Good to Know	"Google Testing Blog – Code Review Best Practices
https://testing.googleblog.com/"	15 mins	Identify maintainability problems.	
	💡 Optional	"Martin Fowler – Refactoring
https://martinfowler.com/books/refactoring.html?utm_source=chatgpt.com"	15 mins	See how experienced engineers improve code over time.	
	💻 Mandatory Practice Exercise				
	"Engineering Scenario: Monday morning. Your Tech Lead asks you to perform the first review of Pull Request #2481 before they approve it.
PR Title: 'Add request-level caching to Product Search'
 
PR Description: 
 • Average search latency reduced from 420ms to 170ms.
 • All automated tests passing.
 • No API contract changes.
 • Feature scheduled for release this week.
 
 Files Changed
 • SearchService.java
 • CacheManager.java
 • SearchController.java
 • SearchServiceTest.java
 
 While reviewing the PR you observe the following excerpts:
  Snippet A
 cache.put(query, result);
  Snippet B
 log.info(""User {} searched {}"", userId, query);
  Snippet C
 String sql = ""SELECT * FROM products WHERE id="" + id;
  Snippet D
 A validation method duplicated from another class.
  Snippet E
 The new cache has no eviction strategy documented.
  Snippet F
 Two important edge cases are not covered by tests.
  Snippet G
 A nested loop executes on every search request.
 
 Reviewer Comments Already Left
  Reviewer A:
 'Looks good to me.'
  Reviewer B:
 'We should use Redis instead.'
  Reviewer C:
 'I'm concerned about stale cache entries.'
 
 Your Tasks
  Phase 1: Review every snippet and decide whether it is:
 • Blocker
 • Should Fix
 • Nice to Have
 • Not an Issue
  Phase 2 : Review the existing reviewer comments.
 State whether you agree or disagree, and justify your reasoning.
  Phase 3 : Write professional review comments that explain:
 • Why the issue matters.
 • What you recommend.
 • How the code could be improved.
  Phase 4 : Recommend one of:
 • Approve
 • Request Changes
 • Approve with Follow-up Actions
 
 Remember: A great code review improves both the code and the teammate—not just the software."				
	📤 How to Record Your Practice Exercise				
	"Create a Pull Request Review Report containing:
 • Executive Summary
 • Findings by Severity
 • Review Comments
 • Responses to Existing Reviewers
 • Questions for the Author
 • Overall Recommendation
 • Risks if Merged
 • Follow-up Actions"				
	🤖 AI Companion (Optional)				
	"Use AI as:
 • The Pull Request author defending design decisions.
 • A Senior Engineer challenging your review.
 • A Security Engineer questioning risk.
 • The Tech Lead asking why you approved or blocked the PR.
 
 AI should challenge your reasoning—not perform the review."				
	✅ How do I know I'm done?				
	" ☐ Mandatory learning completed
 ☐ Every snippet reviewed
 ☐ Existing comments evaluated
 ☐ Review comments are constructive
 ☐ Recommendation justified
 ☐ Pull Request Review Report completed
 
 Self Check
 
 ☐ I can distinguish objective engineering concerns from personal coding preferences.
 ☐ I know when to block a merge and when coaching is more appropriate.
 ☐ I can give feedback that improves both code quality and team collaboration."				
	🚀 Take it Further (Optional)				
	Review one of your own code samples or an AI-generated pull request using the same review template and compare your findings.				
					
	Unit	Unit 11 – Diagnose an Unfamiliar System			
	Guided Practice	Understanding an Unfamiliar Production System			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Understand an unfamiliar production service 
• Identify request flow and dependencies 
• Understand monitoring and operational risks 
• Document assumptions and unknowns 
• Recommend next investigation steps"				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Google SRE Workbook – Troubleshooting
https://sre.google/sre-book/effective-troubleshooting/?utm_source=chatgpt.com"	20 mins	Learn a structured investigation process. Read - Introduction, Theory and Methodology.	
	✅ Mandatory	"OpenTelemetry Documentation – Traces
https://opentelemetry.io/docs/concepts/signals/traces/?utm_source=chatgpt.com"	20 mins	Understand how requests flow through distributed systems.	
	📖 Good to Know	"Google SRE – Monitoring Distributed Systems
https://sre.google/sre-book/monitoring-distributed-systems/?utm_source=chatgpt.com"	15 mins	Interpret dashboards and telemetry.	
	📖 Good to Know	"Atlassian Incident Response Overview
https://www.atlassian.com/incident-management"	15 mins	See how experienced teams investigate ambiguity.	
	💡 Optional	"PagerDuty Incident Response Basics
https://www.pagerduty.com/resources/learn/incident-management/"	15 mins	Understand incident response fundamentals Read only the introductory article.	
	💻 Mandatory Practice Exercise				
	"Engineering Scenario: Monday, 11:53 AM - Customer Support posts in Slack: 'We've received 14 complaints in the last 20 minutes. Some customers cannot complete checkout. Others succeed after refreshing.
Issue appears intermittent.'

Your Tech Lead messages you: 'Please perform the initial investigation. Don't fix anything yet. I need to understand what we're dealing with.'

Engineering Artefacts
Artifact 1 – Slack Discussion
• Customer Support: ""Checkout failures increasing.""
• Backend Engineer: ""We deployed Payment Service this morning.""
• SRE: ""Infrastructure appears healthy.""
• Database Engineer: ""Database CPU is only 32%.""
• Product Manager: ""Most complaints are from Android users.""
Artifact 2 – Dashboard Snapshot
Time Error% p95(ms) Cache Hit%
11:30 0.3 190 91
11:35 0.4 195 90
11:40 1.2 260 84
11:45 5.1 490 62
11:50 2.6 330 74
11:55 0.4 220 91
Artifact 3 – Deployment Timeline
08:30 Recommendation Service
09:40 Payment Service
11:30 Feature Flag Enabled
11:42 Customer errors begin
Artifact 4 – Log Excerpts
11:42:03 Payment timeout. Retry initiated.
11:42:05 Cache miss.
11:42:07 Authentication successful.
11:42:10 NullPointerException.
11:42:11 Retry succeeded.
11:42:14 Cache miss.
11:42:18 Payment timeout.
11:42:21 Inventory lookup completed.
11:42:23 Authentication successful.
11:42:27 Retry succeeded.
11:42:29 Cache miss.
11:42:31 Order completed.
Artifact 5 – Service Flow
Gateway → Checkout → Payment → Inventory → Database

Your Tasks
Phase 1 : Reconstruct the timeline.
Phase 2 : Separate facts from assumptions.
Phase 3 : Identify:
• Likely signals
• Possible noise
• One potential red herring
Phase 4 : Produce THREE ranked hypotheses with confidence (High/Medium/Low).
Phase 5 : For each hypothesis, state what additional evidence would increase or decrease your confidence.
Phase 6 : Recommend the single next engineering action.
(Examples: collect traces, inspect feature flag rollout, increase logging, rollback, continue investigation.)

Important: Do NOT guess the root cause.
Your objective is to recommend the best next action using the available evidence."				
	📤 How to Record Your Practice Exercise				
	"Create a System Diagnosis Report containing:
• Incident Summary
• Timeline Reconstruction
• Facts vs Assumptions
• Signals vs Noise
• Potential Red Herrings
• Ranked Hypotheses (with Confidence)
• Evidence Still Required
• Recommended Next Engineering Action
• Recommended Next Investigation Step
• Rationale"				
	🤖 AI Companion (Optional)				
	"Use AI as:
• The Backend Engineer defending the deployment.
• The SRE challenging your assumptions.
• The Engineering Manager asking why you chose your next action.
• The Product Manager asking whether the feature should be rolled back.

AI should challenge your reasoning—not investigate the incident for you."				
	✅ How do I know I'm done?				
	" ☐ Mandatory learning completed
☐ Timeline reconstructed
☐ Facts separated from assumptions
☐ Signals distinguished from noise
☐ Three hypotheses ranked
☐ Next action justified
☐ System Diagnosis Report completed

Self Check

☐ I avoided confirmation bias.
☐ I did not confuse correlation with causation.
☐ I chose evidence before opinion.
☐ My recommendation reflects the available evidence rather than certainty."				
	🚀 Take it Further (Optional)				
	Propose observability improvements, missing dashboards, additional alerts and documentation improvements for future engineers.				
					
	Unit	Unit 12 – Conduct an Architecture Review			
	Guided Practice	Evaluating Architectural Design Decisions			
	Estimated Time	2 Hours			
	🎯 What should I learn?				
	"By the end of this Guided Practice you should be able to:
• Evaluate an engineering design before implementation.
• Identify hidden assumptions, risks and trade-offs.
• Balance product, engineering, operations and security concerns.
• Decide whether a proposal is ready to build.
• Produce an Architecture Review Recommendation."				
	📚 Learning Path				
	Priority	Resource	Approx. Time	Purpose	
	✅ Mandatory	"Google Engineering Practices – Design Docs
https://google.github.io/eng-practices/?utm_source=chatgpt.com"	20 mins	Understand how engineers review design documents.	
	✅ Mandatory	"AWS Well-Architected Framework (Design Principles)
https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html?utm_source=chatgpt.com"	20 mins	Recognise operational and scalability trade-offs.	
	📖 Good to Know	"Martin Fowler – Evolutionary Architecture
https://martinfowler.com/articles/evo-arch-forward.html"	15 mins	Learn why good designs evolve.	
	📖 Good to Know	"Stripe Engineering – Scaling your API with rate limiters
https://stripe.com/blog/rate-limiters"	15 mins	Learn real-world architecture decisions.	
	💡 Optional	"Thoughtworks Technology Radar
https://www.thoughtworks.com/radar?utm_source=chatgpt.com"	15 mins	See how organisations evaluate technical choices.	
	💻 Mandatory Practice Exercise				
	"Engineering Scenario: Tomorrow morning your team's proposal will be presented to the Architecture Review Board.
Your Tech Lead asks you to review the first draft before the formal review.

Engineering Artefacts:
1. Design document (problem, goals, non-goals, key decisions)
2. System constraints
3. Architecture diagram
4. Stakeholder comments

Tasks:
Phase 1 – Identify assumptions.
Phase 2 – Identify engineering risks and trade-offs.
Phase 3 – Prepare review questions.
Phase 4 – Identify one design decision that could create long-term operational problems.
Phase 5 – Recommend ONE outcome:
• Approve
• Approve with Required Changes
• Reject Pending Rework
Support every recommendation with evidence.

Important: Do not redesign the solution. Your responsibility is to determine whether the proposal is ready to proceed to implementation."				
	📤 How to Record Your Practice Exercise				
	"Prepare an Architecture Review Recommendation containing:
• Executive Summary
• Key Assumptions
• Major Risks
• Trade-offs Identified
• Questions for the Author
• Blocking Concerns
• Positive Aspects
• Recommendation
• Required Changes Before Approval
• Supporting Evidence"				
	🤖 AI Companion (Optional)				
	"Use AI as:
• Proposal author defending design decisions
• SRE questioning operational readiness
• Security Engineer raising compliance concerns
• Product Manager defending deadlines

AI should challenge your reasoning—not perform the review."				
	✅ How do I know I'm done?				
	" ☐ Mandatory learning completed
☐ Assumptions identified
☐ Risks linked to trade-offs
☐ Review questions prepared
☐ Recommendation supported by evidence
☐ Architecture Review Recommendation completed

Self Check
☐ I challenged assumptions respectfully.
☐ I balanced product, engineering, security and operations.
☐ I distinguished evidence from opinion.
☐ I recommended the next engineering decision—not my preferred design."				
	🚀 Take it Further (Optional)				
	Read a public design document or RFC and perform the same architecture review. Compare your concerns with the decisions ultimately made by the engineering team.				
					
# InnoScan PPT Copy Paste Content

Use one section per slide in PowerPoint.
Copy title text into the slide title box.
Copy bullet text into the slide body box.

   

## Slide 1   Title
Title: InnoScan   AI Governed Innovation Intake and Delivery Accelerator
Subtitle:
  Intel x Wipro Hackathon
  Intake  > Similarity Governance  > Approval  > AI Generated Artifacts
  Enterprise POC intake, risk control, and downstream execution

   

## Slide 2   Core Challenge Definition
Title: Core Challenge Definition
Body:
  Enterprises receive many innovation ideas, but intake and evaluation are still mostly manual.
  This leads to duplicate efforts, delayed decisions, and weak traceability from idea to execution.
  Teams spend time on repetitive tasks instead of high value engineering work.

   

## Slide 3   Relevance and Impact
Title: Relevance and Impact
Body:
  The problem affects employees, managers, engineering teams, and business stakeholders.
  If unresolved, organizations face higher costs, slower time to market, and weak governance.
  In regulated or large enterprises, poor auditability increases operational risk.

   

## Slide 4   Alignment with AI Focus
Title: Alignment with AI Focus
Body:
  Semantic similarity detection requires embedding based intelligence, not keyword matching.
  AI assisted retrieval improves decision quality and consistency.
  Generative AI automates SRS and starter code creation at scale.
  This aligns with Intel and Wipro priorities: AI first modernization and responsible automation.

   

## Slide 5   Specific and Measurable Problem
Title: Specific and Measurable Problem
Body:
  For each new POC, determine semantic similarity to existing ideas.
  Route similar ideas to manager exception workflow.
  Convert approved or new ideas into execution ready artifacts.
  Measured by decision latency, exception turnaround time, and artifact generation lead time.

   

## Slide 6   Core Solution Idea
Title: Core Solution Idea
Body:
  InnoScan is a Flask based AI governed innovation workflow platform.
  It captures ideas, runs similarity checks, triggers approvals, and generates artifacts.
  It unifies governance and execution in one pipeline.
  Asynchronous processing enables faster user response and scalable operations.

   

## Slide 7   AI Techniques Used
Title: AI Techniques Used
Body:
  Machine Learning: all MiniLM L6 v2 embeddings for semantic understanding.
  Vector Similarity: Pinecone nearest neighbor matching for related POC detection.
  Generative AI: Qwen APIs for SRS and code generation.
  Intelligent Automation: event driven async pipeline after submission and approval.
  Human in the loop governance: threshold policy with manager decision control.

   

## Slide 8   Value and Impact
Title: Value and Impact
Body:
  Reduces duplicate POC investments.
  Improves governance through auditable exception decisions.
  Accelerates engineering kickoff with auto generated SRS and code scaffolds.
  Augments team productivity beyond traditional form based systems.

   

## Slide 9   System Data Flow
Title: System Data Flow
Body:
  Ingestion: employee submits POC through web UI.
  Persistence: idea saved as JSON.
  Preprocessing: content prepared for embedding and indexing.
  Inference: vector search finds top semantic matches.
  Decision: route to exception flow or continue as new POC.
  Output: approved/new ideas trigger async SRS and optional code generation.

   

## Slide 10   AI Model Invocation
Title: AI Model Invocation
Body:
  Embedding model is called during retrieval and ingestion phases.
  Qwen model APIs are called for SRS generation and code generation.
  Service orchestration ensures the correct order and business rule validation.

   

## Slide 11   Scalable Modular Design
Title: Scalable Modular Design
Body:
  Modular route service structure for auth, submission, and exception workflows.
  Dedicated components for retrieval, ingestion, SRS generation, and code generation.
  Decoupled data stores for uploads, exceptions, knowledge base, and vector index.
  Async processing and API driven modules support enterprise grade scaling.

   

## Slide 12   Technology and Security
Title: Technology and Security
Body:
  Stack: Flask, sentence transformers, LangChain modules, Pinecone, Qwen APIs.
  Data persistence: JSON for transparent and rapid iteration.
  Security controls: role based access and manager approval gates.
  Reliability controls: environment based config, logs, and operational traceability.

   

## Slide 13   Tangible Business Benefits
Title: Tangible Business Benefits
Body:
  Cost reduction from minimizing duplicate initiatives.
  Productivity gains from faster intake to decision cycle.
  Better decision quality via semantic similarity matching.
  Improved employee and manager workflow experience.

   

## Slide 14   Measurable Outcomes
Title: Measurable Outcomes
Body:
  Duplicate leakage reduction percentage.
  Exception SLA compliance percentage.
  Cycle time reduction from submission to approval.
  Time saved for SRS drafting and initial code scaffold setup.
  Existing proof points: operational workflow, threshold routing, and async artifact generation.

   

## Slide 15   Alignment with Trends
Title: Alignment with Trends
Body:
  Aligns with enterprise AI adoption and digital transformation goals.
  Supports human in the loop AI governance.
  Accelerates software delivery lifecycle from idea to documentation and code.
  Enables process automation with measurable business outcomes.

   

## Slide 16   Long Term Value Creation
Title: Long Term Value Creation
Body:
  Builds a compounding, searchable enterprise POC knowledge base.
  Improves retrieval quality as approved data grows.
  Standardizes governance across innovation teams.
  Creates a foundation for portfolio analytics and strategic planning.

   

## Slide 17   Proof of Execution
Title: Proof of Execution
Body:
  Implemented role based login and user journeys.
  Delivered submission, similarity, exception, and approval flows.
  Integrated knowledge base persistence and vector ingestion.
  Implemented automated SRS generation and optional code generation.
  Materialized generated code into project folder structures.

   

## Slide 18   Performance Metrics
Title: Performance Metrics
Body:
  Show sample similarity scores and threshold routing behavior.
  Show end to end timestamps from submit to generated artifacts.
  Show generation success rates for SRS and code outputs.
  If needed, present preliminary values with assumptions clearly labeled.

   

## Slide 19   User Workflows
Title: User Workflows and Team Execution
Body:
  Employee flow: submit idea  > review similarity  > request exception if needed.
  Manager flow: review queue  > inspect details  > approve or reject.
  System flow: persist  > retrieve  > decide  > ingest  > generate asynchronously.
  Team delivered integrated web + AI + generation workflow under hackathon constraints.

   

## Slide 20   Building Confidence
Title: Building Confidence
Body:
  End to end architecture is functional and demonstrable.
  Modular design supports hardening, extension, and scaling.
  Logs and artifacts provide transparent execution evidence.
  Clear roadmap exists for enterprise controls and production readiness.

   

## Slide 21   Recap
Title: Recap Key Messages
Body:
  Problem: innovation intake is slow, duplicative, and difficult to govern.
  Solution: AI governed workflow with semantic similarity and exception management.
  Value: faster decisions, lower waste, stronger governance, faster execution.

   

## Slide 22   Next Steps
Title: Next Steps
Body:
  Add analytics dashboards for throughput and SLA monitoring.
  Tune similarity confidence and thresholds by domain.
  Strengthen scale architecture with queueing, retries, and observability.
  Integrate with enterprise ticketing, CI/CD, and project systems.
  Expand security and compliance controls for production rollout.

   

## Slide 23   Thank You
Title: Thank You
Body:
  Thank you to the organizers, mentors, and jury.
  We appreciate your time and feedback.
  Open to questions and next stage collaboration.

   

## Compact Bullet Pack (For Limited Slide Space)

### 1) Problem
  Manual POC intake causes delay and duplication.
  Similar ideas are missed early.
  Governance and audit trails are weak.

### 2) Relevance
  Impacts employees, managers, and engineering teams.
  Increases cost and slows time to market.
  Creates execution and compliance risk.

### 3) Why AI
  Embeddings detect semantic similarity better than keywords.
  GenAI accelerates SRS and code generation.
  Human in the loop keeps governance controlled.

### 4) Specific + Measurable
  Detect similarity for every submission.
  Route exceptions for manager decisions.
  Measure latency, SLA, and artifact lead time.

### 5) Solution
  One platform for intake, similarity, approval, and generation.
  Async pipeline for faster user response.
  Modular architecture for scale.

### 6) AI Stack
  all MiniLM L6 v2 for embeddings.
  Pinecone for vector similarity search.
  Qwen APIs for SRS and code generation.

### 7) Architecture Flow
  Submit  > Store  > Embed  > Match  > Decide.
  Approve/New  > Ingest  > Generate SRS  > Generate Code.
  Materialize project scaffold automatically.

### 8) Business Value
  Lower duplicate effort and cost.
  Faster decision and delivery cycles.
  Better quality and user experience.

### 9) Proof + Metrics
  End to end workflow is implemented.
  Similarity and exception routing are working.
  Track scores, SLA, cycle time, and generation success.

### 10) Close
  Recap: problem, AI solution, business impact.
  Next: scale, integrations, observability, compliance.
  Thank jury, mentors, and organizers.

   

## 10 Slide Judge Pitch (Max 3 Bullets + Speaker Note)

### Slide 1   Title and Hook
Title: InnoScan   AI Governed Innovation Intake
Bullets:
  AI pipeline from idea intake to execution artifacts.
  Built for enterprise governance and speed.
  Intel x Wipro Hackathon solution.
Speaker Note: We solve a common enterprise bottleneck: innovation ideas are collected, but not converted to governed execution fast enough.

### Slide 2   Core Problem
Title: Core Challenge
Bullets:
  Manual intake creates delays and inconsistency.
  Duplicate ideas slip through without semantic checks.
  Weak traceability from submission to execution.
Speaker Note: The current process wastes time, duplicates effort, and makes governance difficult.

### Slide 3   Why It Matters
Title: Relevance and Impact
Bullets:
  Affects employees, managers, and engineering teams.
  Increases cost and slows time to market.
  Raises operational and compliance risk.
Speaker Note: If unresolved, this problem directly reduces innovation ROI and execution confidence.

### Slide 4   AI Fit and Strategic Alignment
Title: Why AI + Intel/Wipro Alignment
Bullets:
  Embeddings enable semantic similarity detection.
  GenAI automates SRS and code scaffolding.
  Supports AI first, responsible enterprise automation.
Speaker Note: This is a strong AI use case with clear alignment to enterprise modernization priorities.

### Slide 5   Solution Overview
Title: Core Solution Idea
Bullets:
  Submit idea  > similarity check  > exception workflow.
  Approved/new ideas trigger SRS and code generation.
  Unified governance + delivery pipeline.
Speaker Note: InnoScan combines decision governance and execution acceleration in one flow.

### Slide 6   Architecture and Data Flow
Title: System Data Flow
Bullets:
  Ingest and store submission as structured JSON.
  Embed and match in Pinecone for top semantic hit.
  Route decision, then asynchronously generate artifacts.
Speaker Note: We designed the architecture to separate real time decisions from heavier background generation.

### Slide 7   AI Techniques and Model Invocation
Title: AI Techniques Used
Bullets:
  all MiniLM L6 v2 embeddings for similarity.
  Pinecone vector search for retrieval.
  Qwen APIs for SRS and code generation.
Speaker Note: We use a hybrid pattern: deterministic workflow controls plus AI driven intelligence.

### Slide 8   Business Value and Measurable Outcomes
Title: Value and KPI Impact
Bullets:
  Reduces duplicate effort and operating cost.
  Improves decision speed and governance quality.
  Track SLA, cycle time, and generation success rate.
Speaker Note: Value is measurable through operational KPIs, not just qualitative feedback.

### Slide 9   Proof of Execution
Title: Demo Readiness and Results
Bullets:
  End to end workflow is implemented and functional.
  Similarity routing and manager approvals are working.
  Async SRS/code generation pipeline is active.
Speaker Note: We are not showing a concept only; we are showing a working integrated system.

### Slide 10   Recap and Next Steps
Title: Recap + Forward Plan
Bullets:
  Problem solved: governed, AI driven innovation intake.
  Value delivered: faster, cheaper, more auditable execution.
  Next: scale architecture, integrations, and compliance hardening.
Speaker Note: Thank you to the jury, mentors, and organizers; we are ready for the next stage.

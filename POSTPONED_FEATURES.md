# V.E.R.D.A.N.T. — Postponed Features & Future Roadmap (V2+)
### Deliberate Non-MVP Scope Boundaries & Post-Hackathon Architecture

> **Guiding Principle:**  
> These are high-value capabilities that belong in a production enterprise platform, but are deliberately deferred from the MVP to eliminate fragile complexity and guarantee a 100% stable, flawless live demo on hackathon day.

---

## 1. Postponed Feature Inventory & Strategic Rationale

| # | Feature | Why It Is Postponed from MVP | When It Will Be Introduced |
| :- | :--- | :--- | :--- |
| **1** | **Bug Knowledge Memory** | Requires a historical dataset of hundreds of verified bug-fix pairs to be useful. | **Phase 2 (Post-Launch)** once the platform logs real-world sessions. |
| **2** | **Advanced Green Analytics Dashboard** | High-fidelity interactive dashboards with custom widgets add UI drag. Basic Wh and ml water reporting is sufficient. | **Phase 2** for enterprise ESG reporting. |
| **3** | **Universal Website & Framework Support** | Supporting arbitrary legacy frameworks (AngularJS, PHP, jQuery, Canvas apps) will consume all dev time. | **Phase 3**; MVP strictly targets modern SPAs/SSRs (**React, Next.js, Vue**). |
| **4** | **Multi-Language AST Analysis** | Building AST parsers for Python, Go, Java, and Rust simultaneously is premature scope creep. | **Phase 2**; MVP strictly targets **TypeScript / JavaScript**. |
| **5** | **Zero-Copy Serialization** | High-performance memory management between processes adds C/Rust complexity without changing the demo outcome. | **Phase 3** when scaling to thousands of concurrent users. |
| **6** | **Advanced Streaming Architecture** | Real-time byte streaming creates race conditions during live presentations. | Standard **asynchronous queue processing** is sufficient for MVP. |
| **7** | **Complex Dependency Graph Resolution** | Resolving entire monorepo transitive dependency conflicts is an entire product in itself. | **Phase 2**; MVP targets the directly imported component file. |
| **8** | **Full Monorepo Regression Testing** | Running 2,000 unit tests across an entire monorepo slows the demo down by 10 minutes. | **Phase 2**; MVP runs only the **affected component test suite**. |
| **9** | **Calibrated Numerical Confidence Model** | Exact percentages (e.g. `92.4%`) require statistical training against ground-truth benchmarks. | **Phase 2**; MVP uses a defensible **`LOW / MEDIUM / HIGH`** rating based on evidence count. |
| **10** | **Bug Knowledge Graph (Neo4j / Graph RAG)** | Graph databases require ongoing maintenance and indexing infrastructure. | **Phase 3** as an enterprise knowledge asset. |
| **11** | **Advanced PR Micro-Optimizations** | Auto-formatting PR descriptions and commit rebasing is secondary to basic patch correctness. | **Phase 2**; MVP creates a clean, standard **Draft PR**. |
| **12** | **Autonomous Multi-Agent Orchestration** | Multi-agent swarms frequently deadlock or hallucinate recursive loops under pressure. | **Phase 3**; MVP uses a **deterministic single-pipeline architecture**. |

---

## 2. Why Postponing These Features Wins the Buildathon

1. **Zero Demo Crashes:** Complex systems fail at the seams. Removing multi-agent swarms and zero-copy buffers eliminates the #1 cause of live hackathon demo crashes.
2. **Speed to Deliver:** The team focuses 100% of engineering bandwidth on the **15 core MVP checklist items**.
3. **Credibility with Judges:** When judges ask: *"Does this work with Java or legacy PHP?"*, your answer is sharp and confident:  
   > *"No, we deliberately scoped our MVP to modern React/Next.js web applications to guarantee 100% reproduction accuracy before expanding to our Phase 2 multi-language AST roadmap."*  
   Judges will immediately recognize real product management discipline.

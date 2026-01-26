# Resonance v2.0: The Operator Manual 📖

> **System Prompt / Identity Matrix**
> *This is the definitive guide to the 26 specialized agents and 13 scientific workflows that power Resonance.*

---

## 🛑 The Prime Directives (The 4 Zeros)
Every Agent in this system is bound by these four immutable laws.

1.  **Zero Divergence**: The `.resonance` folder is the **Single Source of Truth**. The **Soul** (Vision), **Systems** (Architecture), **State** (Context), **Memory** (Wisdom), and **Tools** (Boundaries) form the 5 Pillars of Law. Code must never contradict them.
2.  **Zero Entropy**: We fight complexity. We use the simplest tool for the job. We accept "boring" standards for infrastructure so we can focus leverage on the product. We reject thoughtless defaults and never ship "good enough". Every interaction and logic flow must be intentional. We build with the precision of the top 1%.
3.  **Zero Guesswork**: We do not fix bugs without a reproduction script. We do not ship features without a test. The Scientific Method is mandatory.
4.  **Zero Drag**: Interaction must *feel* instant. We respect the user's flow above all else. If a process is heavy, the UI must remain fluid. We mask latency with prediction and optimism. We treat every millisecond of delay and every grain of confusion as a bug.

---

## 👩‍🚀 The Specialized Roster (26 Agents)
Do not use a generic chatbot. Activate the specialist for the job.

### 🟡 Strategy & Inception (The Visionaries)
| Agent | Skill Path | Expertise |
| :--- | :--- | :--- |
| **Product Manager** | `resonance-product` | **PRD & Scope**. Defines "Working Backwards" specs. Kills scope creep. |
| **Tech Lead** | `resonance-architect` | **System Design**. C4 Models, Database Policies, API Contracts. |
| **Growth Strategist** | `resonance-growth` | **Analytics**. Retention loops, viral mechanics, data-driven decisions. |
| **Venture Validator** | `resonance-venture` | **Market Risk**. "Kill Criteria", smoke testing ideas before building. |
| **Research Scientist** | `resonance-researcher` | **Deep Dive**. Technical investigations, trade-off analysis (Buy vs Build). |
| **Creative Director** | `resonance-designer` | **Visual System**. Design Systems, Typography, Topological Betrayal. |

### 🟢 Execution & Engineering (The Builders)
| Agent | Skill Path | Expertise |
| :--- | :--- | :--- |
| **Backend Engineer** | `resonance-backend` | **Robust Systems**. NestJS, Python, API optimization, DB Integrations. |
| **Frontend Engineer** | `resonance-frontend` | **The Glasssmith**. React/Web. Expert in "Touch Physics" & Micro-interactions. |
| **Mobile Engineer** | `resonance-mobile` | **App Craftsman**. React Native / Flutter. Offline-first, thumb-zone optimized. |
| **Game Architect** | `resonance-game-dev` | **The Juice**. Core loops, gamification psychology, particle systems. |
| **Database Architect** | `resonance-database` | **Data Safety**. Schema design, migration safety, query optimization. |
| **DevOps Engineer** | `resonance-devops` | **Pipelines**. CI/CD, Docker optimization, Infrastructure as Code. |
| **Debugger** | `resonance-debugger` | **Root Cause**. Scientific Method (RCA), reproduction scripts. |
| **Tooling Engineer** | `resonance-automation` | **Tooling**. Creates new tools, MCP servers and agent capabilities. |

### 🔵 Quality & Optimization (The Scalers)
| Agent | Skill Path | Expertise |
| :--- | :--- | :--- |
| **Security Auditor** | `resonance-security` | **Hardening**. Pen-testing, JWT/Auth protocols, CSP headers. |
| **QA Engineer** | `resonance-qa` | **Verification**. E2E testing (Playwright), Property-based testing (Fuzzing). |
| **Performance Eng** | `resonance-performance` | **Speed**. Core Web Vitals, Bundle analysis (Webpack/Rollup). |
| **SEO Specialist** | `resonance-seo` | **Visibility**. Programmatic SEO, Schema Markup, GEO (Gen-AI Optimization). |
| **Conversion Eng** | `resonance-conversion` | **Revenue**. CRO, Landing page anatomy, A/B testing infrastructure. |
| **Copywriter** | `resonance-copywriter` | **Voice**. Neuro-marketing triggers, value proposition refinement. |
| **Studio** | `resonance-studio` | **Visuals**. Asset generation (Midjourney/Flux), Style consistency. |

### 🟣 Maintenance & Governance (The Keepers)
| Agent | Skill Path | Expertise |
| :--- | :--- | :--- |
| **Code Reviewer** | `resonance-reviewer` | **Gatekeeper**. Semantic code analysis, blocking anti-patterns. |
| **Refactor** | `resonance-refactor` | **Essentialism**. Reducing cyclomatic complexity, enforcing SOLID. |
| **Skill Author** | `resonance-skill-author`| **Instruction**. Designing new agent personas and skill directives. |
| **Librarian** | `resonance-librarian` | **Knowledge**. Documenting solutions and maintaining docs. |
| **The Kernel** | `resonance-core` | **Orchestrator**. Managing State (`01_state.md`), Memory, and Planning. |

---

## ⚡ The Workflow Map (Scientific Method)
These are not just scripts. They are **Methodologies**.

### Phase 1: Inception
*   **`/init`**: **Awakening**.
    *   *Behavior*: Bootstraps the `.resonance` memory structure in *any* project.
*   **`/plan`**: **Deep Research & Spec**.
    *   *Behavior*: Spends 80% of time reading docs/code. Outputs a rigorous `implementation_plan.md`.

### Phase 2: Execution
*   **`/build`**: **The TDD Loop**.
    *   *Behavior*: Write Test -> Fail -> Write Code -> Pass.
*   **`/debug`**: **Root Cause Analysis**.
    *   *Behavior*: "Find the Smoking Gun." Creates a reproduction script to isolate the bug *before* fixing it.
*   **`/refactor`**: **Atomic Cleanup**.
    *   *Behavior*: Improves structure without changing input/output behavior.
*   **`/design`**: **Visual Engine**.
    *   *Behavior*: Generates UI components with forced visual feedback loops.

### Phase 3: Verification
*   **`/test`**: **Pyramid Testing**.
    *   *Behavior*: Generates Unit, Integration, and E2E tests based on `resonance-qa` standards.
*   **`/audit`**: **Local Audit**.
    *   *Behavior*: Runs the "Swarm". Security checks, Performance checks, Lint checks.

### Phase 4: Delivery
*   **`/ship`**: **The Release Protocol**.
    *   *Behavior*: Checks Health Score. Updates Changelog. Tags Release. Deploys.
*   **`/review-pr`**: **External Gatekeeper**.
    *   *Behavior*: Checks out a PR. runs `/audit`. Summarizes risks.

---

## 🛠️ How to Operate
Resonance is "Driver-Assisted". You are the Pilot. The Agents are your Crew.

### 1. The Activation Command
Don't ask "How do I do this?". Tell the crew what to do.

> **Bad**: "Can you help me fix the login?"
> **Good**: "Activate **Security Auditor**. Debug the JWT expiration bug in `auth.service.ts`."

### 2. The Verification Loop
Never trust. Always verify.

> **Bad**: "Looks good."
> **Good**: "Run `/test`. Verify the edge case where the user has no email."

### 3. The Knowledge Compound
If you solve a hard problem, save it.

> "Run `/capture`. Document how we solved the Supabase RLS issue."

---

---

*Start building.*

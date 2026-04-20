# Protocol: C4 Architecture Diagrams
> **Objective**: Standardize system visualization using the C4 Model (Context, Containers, Components, Code) and Mermaid syntax.
> **Philosophy**: "Context + Container diagrams are sufficient for 95% of documentation."

## 1. The Hierarchy (When to use what)

| Level | Diagram Type | Audience | Shows | Requirement |
|-------|-------------|----------|-------|-------------|
| **1** | **System Context** | Executives/All | System + Users + External Systems | **Mandatory** |
| **2** | **Container** | Architects/Devs | Apps, Databases, Microservices | **Mandatory** |
| **3** | **Component** | Developers | Internal Modules/Classes | *Optional* (Complex logic only) |
| **4** | **Code** | Developers | UML Classes | *Rare* (Use code instad) |

---

## 2. Templates (Copy-Paste)

### Level 1: System Context
*The Big Picture. No technical details (no "SQL", no "React"). Just "User", "System", "External System".*

```mermaid
C4Context
  title System Context - [System Name]

  Person(user, "User", "A customer utilizing the platform")
  System(system, "Resonance Platform", "The core agent functionality")
  System_Ext(auth0, "Auth Provider", "Handles identity and access")

  Rel(user, system, "Uses")
  Rel(system, auth0, "Authenticates via")
```

### Level 2: Container Diagram
*The Technical Architecture. "What is running?" (Docker containers, Databases).*

```mermaid
C4Container
  title Container Diagram - [System Name]

  Person(user, "User", "Uses the app")

  System_Boundary(c1, "Resonance Core") {
    Container(web_app, "Web App", "Next.js/React", "Frontend Interface")
    Container(api, "API Gateway", "Node.js/Express", "Handles requests")
    ContainerDb(db, "Database", "PostgreSQL", "Stores user data")
    ContainerQueue(queue, "Job Queue", "Redis", "Async tasks")
  }

  Rel(user, web_app, "HTTPS")
  Rel(web_app, api, "JSON/REST")
  Rel(api, db, "SQL", "Read/Write")
  Rel(api, queue, "Enqueues")
```

### Level 3: Component Diagram
*The Module Structure. Only use for complex containers (e.g., a "Pricing Engine").*

```mermaid
C4Component
  title Component Diagram - API Service

  Container(controller, "Controller", "Express", "Validates Input")
  Container(service, "Service Layer", "Class", "Business Logic")
  Container(repo, "Repository", "Class", "Data Access")

  Rel(controller, service, "Calls")
  Rel(service, repo, "Persists")
```

---

## 3. Best Practices
1.  **Unidirectional Flow**: Arrows should generally flow Left -> Right or Top -> Bottom. Avoid cycles.
2.  **Action Verbs**: Label every relationship. `Rel(a, b, "Uses")` is weak. `Rel(a, b, "Publishes events to")` is strong.
3.  **Tech Labels**: In Container diagrams, ALWAYS specify technology (e.g., "PostgreSQL", "React", "gRPC").

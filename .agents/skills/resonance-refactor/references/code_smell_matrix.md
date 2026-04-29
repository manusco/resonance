# Code Smell Matrix

> "If it smells, name what breaks."

| Smell | Definition | Business Risk (What Breaks) | The Fix (Recipe) |
| :--- | :--- | :--- | :--- |
| **God Class** | A class that does everything (e.g., `UserManager`). | Access rules, billing logic, and profile updates will silently drift when any one responsibility changes. A bug fix in billing accidentally changes auth behavior. | **Extract Class**. Identify responsibilities (Auth, Profile, Billing) and split. |
| **Long Method** | A function > 20 lines. | Bugs hide in deeply nested branches. New developers cannot safely modify the function without understanding all paths. | **Extract Method**. Highlight a block -> Right Click -> Refactor. |
| **Shotgun Surgery** | Changing one thing requires edits in 5 files. | Adding a new field or role requires coordinated edits across multiple files. One will be missed, creating a silent inconsistency. | **Move Method**. Co-locate the data and the logic. |
| **Primitive Obsession** | Using `string` for everything (e.g., Phone Number). | Invalid values bypass validation because the type doesn't enforce constraints. "123" is accepted as an email because it's just a string. | **Replace Data Value with Object**. Create a `PhoneNumber` class (Value Object). |
| **Feature Envy** | Method A uses data from Class B more than its own. | Changes to Class B's structure break Method A. The dependency is invisible until it fails. | **Move Method**. The method belongs in Class B. |
| **Comments as Deodorant** | Explaining *what* code does (e.g., `// Increment i`). | The comment drifts from reality as code changes. Future developers trust the comment over the code and introduce bugs. | **Rename Method/Variable**. Code should explain itself. |
| **Duplicated Access Logic** | Permission checks scattered across routes, policies, and templates. | Adding a new role requires updating checks in N locations. Miss one, and users get wrong access. Authorization drift is a security risk. | **Centralize**. Create a single capability/policy system. |
| **Duplicated Persistence Mapping** | Same field mapped in ORM model AND raw SQL query. | Schema change updates one mapping but not the other. Data silently corrupts or queries return stale results. | **Single Source**. Use one mapping layer (ORM or raw, not both). |

## The Mandate

*   **Zero Tolerance**: If you spot a God Class, you must at least *plan* its destruction (Mikado Method).
*   **Always Name the Risk**: Never report a smell without stating the concrete business consequence. "Feature envy" alone is not a finding. "Feature envy: `OrderController.calculateTax()` uses 6 fields from `TaxService` — when tax rules change, this method will break silently" is a finding.

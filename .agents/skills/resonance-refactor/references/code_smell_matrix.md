# Code Smell Matrix

> "If it smells, clean it."

| Smell | Definition | The Fix (Recipe) |
| :--- | :--- | :--- |
| **God Class** | A class that does everything (e.g., `UserManager`). | **Extract Class**. Identify responsibilities (Auth, Profile, Billing) and split. |
| **Long Method** | A function > 20 lines. | **Extract Method**. Highlight a block -> Right Click -> Refactor. |
| **Shotgun Surgery** | Changing one thing requires edits in 5 files. | **Move Method**. Co-locate the data and the logic. |
| **Primitive Obsession** | Using `string` for everything (e.g., Phone Number). | **Replace Data Value with Object**. Create a `PhoneNumber` class (Value Object). |
| **Feature Envy** | Method A uses data from Class B more than its own. | **Move Method**. The method belongs in Class B. |
| **Comments as Deodorant** | Explaining *what* code does (e.g., `// Increment i`). | **Rename Method/Variable**. Code should explain itself. |

## The Mandate

*   **Zero Tolerance**: If you spot a God Class, you must at least *plan* its destruction (Mikado Method).

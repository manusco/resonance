# SOLID Principles Protocol

> "Robust, maintainable, flexible."

## 1. SRP (Single Responsibility)
*   **A class should have one reason to change.**
*   *Violation*: `UserManager` handles DB saves AND Email sending.

## 2. OCP (Open/Closed)
*   **Open for extension, Closed for modification.**
*   *Strategy*: Use Interfaces/Polymorphism instead of massive `switch` statements.

## 3. LSP (Liskov Substitution)
*   **Subtypes must be substitutable for base types.**
*   *Violation*: `Square` inherits `Rectangle` but throws error on `setWidth`.

## 4. ISP (Interface Segregation)
*   **Client should not be forced to depend on methods it doesn't use.**
*   *Strategy*: Split `IWorker` into `IEat` and `IWork`.

## 5. DIP (Dependency Inversion)
*   **Depend on Abstractions, not Concretions.**
*   *Code*: Inject `IDatabase`, not `PostgresDatabase`.

> 🔴 **Rule**: If you have to touch a Core Class to add a Plugin, you failed OCP.

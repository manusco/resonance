# Domain Driven Design (DDD) Protocol

> "Tackle complexity in the heart of software."

## 1. Strategic Design (The Big Picture)

1.  **Ubiquitous Language**:
    *   The code MUST speak the language of the business.
    *   If the Expert says "Book a Shipment", the code MUST be `shipmentService.book()`, NOT `dataManager.saveRow()`.
2.  **Bounded Contexts**:
    *   Draw strict boundaries.
    *   `User` in **Sales Context** (Lead) != `User` in **Support Context** (Ticket Owner).
    *   Do NOT create a single giant `User` class for the whole system.

## 2. Tactical Design (The Building Blocks)

1.  **Entities**:
    *   Have an Identity (ID).
    *   Mutable. (e.g., A `User` changes email, but is the same user).
2.  **Value Objects**:
    *   No Identity. Defined by attributes.
    *   Immutable. (e.g., `Address`, `Money`, `DateRange`).
    *   If you change a property, you create a NEW object.
3.  **Aggregates**:
    *   A cluster of objects treated as a unit.
    *   Root Entity controls access.
    *   Result: `Order` (Root) contains `LineItems`. You cannot access `LineItem` directly; you must go through `Order`.

## 3. The Anemic Model Ban

**Forbidden**:
*   Classes that are just getters/setters (Data Bags) with zero logic.
*   Logic living entirely in "Services".

**Required**:
*   Rich Domain Models. `Order.addItem()` should check inventory and recalculate total itself.

> 🔴 **Rule**: Logic belongs in the Domain Object, not the Service, whenever possible.

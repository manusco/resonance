# Atomic Design Protocol

> "We're not designing pages, we're designing systems of components."
> — Brad Frost

## 1. The Hierarchy

1.  **Atoms**: Cannot be broken down. (Label, Input, Button).
2.  **Molecules**: Groups of atoms. (Search Form: Label + Input + Button).
3.  **Organisms**: Complex sections. (Header: Logo + Nav + Search Form).
4.  **Templates**: Wireframes.
5.  **Pages**: Real content instances.

## 2. The Directory Structure

```
components/
  atoms/
    Button.tsx
    Input.tsx
  molecules/
    SearchForm.tsx
  organisms/
    Header.tsx
```

## 3. The Composition Rule

*   **Organisms** can contain **Molecules** and **Atoms**.
*   **Molecules** can contain **Atoms**.
*   **Atoms** contain NO other components (only HTML).

> 🔴 **Rule**: A Molecule should not define margin/layout. The Parent (Organism) defines the layout.

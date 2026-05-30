# Degrees of freedom (match constraint to fragility)

The core authoring decision: how much to pin down. Too loose and fragile steps break;
too tight and you waste tokens telling a smart model things it knows.

Think of the model as a robot crossing terrain:

- **Narrow bridge, cliffs both sides** → one safe path. Give exact, low-freedom instructions. (Database migrations, release steps, anything destructive or order-sensitive.)
- **Open field** → many paths work. Give direction and trust the model. (Code review, drafting, design exploration.)

| Freedom | Form | Use when |
| :-- | :-- | :-- |
| **High** | prose heuristics | multiple valid approaches; context decides |
| **Medium** | parameterized script / pseudocode | a preferred pattern exists, config varies |
| **Low** | exact script, run verbatim | fragile, order-critical, must be identical every time |

## The smart-agent assumption

The model is already capable. Only add what it does not have: your project's
conventions, the non-obvious gotcha, the exact command. Cut anything it would do
anyway. For every paragraph ask: "does this justify its tokens?"

## Concrete

High (let it judge):
```
Review the diff for correctness bugs and missing edge cases, then for simplifications.
```

Low (do not deviate):
```
Run exactly: python scripts/migrate.py --verify --backup
Do not add flags or reorder.
```

## Weaker models need less freedom

When compiling for open-weight or smaller models (the open-weights overlay), shift
left: convert high-freedom prose into explicit numbered steps and mandatory verify
commands. The same template, lower freedom, via the overlay.
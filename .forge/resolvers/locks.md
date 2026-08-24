## Operating Locks

Four constraints on every task, regardless of domain. Not preferences. Locks.

- **Think first.** State assumptions before acting. If the request has more than one reading, surface the options; do not pick one silently.
- **Simplicity.** The minimum that solves the problem. No speculative abstractions, no features nobody asked for. A senior reviewer should not call it overbuilt. After understanding the request and tracing the touched flow, stop at the first sufficient option: remove work that is not needed, reuse existing code, use the standard library, use a native platform capability, reuse an installed dependency, compose the shortest clear expression, then add new custom machinery only when the earlier options do not satisfy the contract.
- **Surgical.** Touch only what the task asks for. Match the surrounding style. Do not reformat or "improve" adjacent code in passing.
- **Verify.** Define success before starting. Loop until proven, not until it looks right. No commit without evidence.

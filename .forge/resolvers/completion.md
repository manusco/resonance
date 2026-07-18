## Completion

End every run with a status backed by evidence (output, a passing test, a diff), not "looks right".

- DONE: complete, evidence shown.
- DONE_WITH_CONCERNS: complete; list side effects or debt.
- DONE_PENDING_OUTCOME: the work shipped and is verified as far as it can be in-session, but its real proof is a metric that only lands later (a reply rate, a conversion, a renewal, a page's traffic). Use this instead of DONE when the ground truth is an external outcome you cannot observe now. Record it in the ledger as an `exp-` entry (or a `met-` once the value is known) with a `due:` date, the day the outcome should be checked in; `py .forge/measurement_due.py` surfaces it then. It is not DONE until that outcome is checked in. Code with an in-session executed check is DONE, not this.
- BLOCKED: state the blocker and what you tried.
- NEEDS_CONTEXT: state exactly what is missing.

Escalate (STOP) if a fix failed 3 times, the change is security-sensitive and you are not certain, or scope exceeds what you can verify.

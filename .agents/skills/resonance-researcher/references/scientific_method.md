# Scientific Method Protocol

> "Nullius in verba" (Take nobody's word for it).
> — Royal Society Motto

## 1. The Cycle

1.  **Observation**: "The system is slow." (Vague).
2.  **Hypothesis**: "The DB query on the dashboard is missing an index." (Specific, Falsifiable).
3.  **Prediction**: "If I add an index to `user_id`, latency will drop < 100ms."
4.  **Experiment**: Add the index. Measure.
5.  **Conclusion**: "Latency dropped to 50ms. Hypothesis confirmed."

## 2. The Mandate

**You MUST define the Hypothesis BEFORE you research.**

*   ❌ "I'm looking into libraries." (Wandering).
*   ✅ "I hypothesize that `shadcn/ui` is superior to `MUI` because it allows direct code ownership."

## 3. Verification

*   If you cannot **measure** the result, you didn't do science. You did art.
*   Research without a conclusion is just noise.

> 🔴 **Rule**: Start every investigation with a Hypothesis. End with a Verdict.

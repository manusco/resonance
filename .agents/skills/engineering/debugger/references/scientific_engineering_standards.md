# Scientific Engineering Standards (Zero Guesswork)

This reference defines the strict standards for "Zero Guesswork" engineering, combining the Kdense critical thinking framework with Osmani performance protocols.

## 1. The "No Fix Without Root Cause" Rule
You must NEVER apply a patch or fix without first confirming the root cause.
- **Symptom**: "The API timed out."
- **Bad Fix**: Increase the timeout to 30 seconds.
- **Root Cause**: The database query is missing an index, causing a full table scan that takes 15 seconds.
- **Good Fix**: Add the database index.

## 2. Hypothesis-First Execution
Before changing any code, you must formulate a hypothesis.
1. **Observe**: What is the exact error or behavior?
2. **Hypothesize**: "I believe the error is caused by X because of Y."
3. **Alternative Hypothesis**: "If it is not X, it might be Z." (This mitigates Confirmation Bias).
4. **Test**: Write a script or assertion that proves X is the cause.
5. **Execute**: Only apply the fix once the test confirms the hypothesis.

## 3. Cognitive Bias Checklist
When debugging complex issues, engineers are prone to bias:
- **Anchoring**: Did you fixate on the very first error log you saw, ignoring subsequent warnings that might be the true root cause?
- **Availability Heuristic**: Are you assuming it's a CORS issue just because you dealt with a CORS issue yesterday?
- **Confirmation Bias**: Are you only looking for evidence that supports your theory, rather than trying to disprove it?

## 4. Performance as Correctness
A system that is slow is a system that is broken. Performance is not a feature; it is a baseline requirement.
- **N+1 Queries**: Are strictly prohibited. If a loop executes a database query, it is an architectural failure. Use Dataloaders or `JOIN` statements.
- **Hydration Overhead**: Shipping megabytes of unused JavaScript to the client is a failure.
- **Core Web Vitals**: Treat LCP, INP, and CLS as strict compiler errors. If they fail, the build fails.

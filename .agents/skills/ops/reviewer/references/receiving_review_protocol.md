# Receiving Review: technical rigor over performative agreement

> Reviewer and author both serve the same goal: correct code that solves the real problem. Agreeing fast is not the goal. Being right is.

Giving a good review is one skill. Taking one is another, and it is where most quality leaks. The failure mode is not defensiveness, it is the opposite: reflexive agreement. An agent that answers every comment with "You're absolutely right, fixing now" and implements it unverified will happily add dead code, break working behavior, and follow a reviewer's mistaken assumption straight into a regression.

## Banned responses

Do not open a reply with any of these before you have verified the claim against the actual code:

- "You're absolutely right!"
- "Great catch, fixing now."
- "Let me implement that right away."

These are performative agreement. They signal compliance, not understanding, and they commit you to a change you have not checked.

## The response pattern

For each review comment, in order:

1. **Restate** the requirement in your own words. If you cannot, you do not understand it yet, so ask.
2. **Verify** it against the codebase reality. Open the file. Is the claim true here, in this code, as it actually runs? Reviewers work from a diff and can miss context.
3. **Evaluate** whether it is correct for THIS codebase: does it break existing behavior, does it contradict a deliberate earlier decision, does it hold on every target platform?
4. **Respond**: acknowledge and implement, or push back with technical reasoning. Both are valid outcomes. A reasoned disagreement is a better result than a wrong change made politely.
5. **Implement** one item at a time, and verify each before moving to the next. A batch of ten unverified fixes is ten new hypotheses.

## Push back when the code is right

If a comment is wrong for this codebase, say so plainly and show why: the line it would break, the reason the current form exists, the platform where the suggestion fails. Deferring to a mistaken reviewer to avoid friction is a failure of the review, not a courtesy.

## Apply the YAGNI check to suggestions

Reviewers sometimes suggest "do this properly" or "make this generic for later". Before adding the abstraction, grep for the actual usage. If nothing needs it today, the correct response is to remove the speculative code, not to build the generality. The rule cuts both ways: it applies to the reviewer's additions as much as to yours.

## The standard

Answer to the code, not to the reviewer's status. The measure of a received review is whether the merged result is more correct, not whether the conversation felt agreeable.

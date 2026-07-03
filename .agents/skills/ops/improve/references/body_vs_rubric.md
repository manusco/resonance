# Body vs Rubric: which is the weak link

> A flat score (skill and no-skill tie) has two very different causes. The skill may not add enough over the base model (weak body), or the eval may be too blunt to see the value the skill already adds (coarse rubric). Fixing the wrong one wastes the pass, so diagnose first.

## Read both outputs before deciding

Look at the graded with-skill and without-skill answers side by side.

- If the with-skill answer is clearly better but scored the same, the RUBRIC is the problem. It is not testing the thing the skill improved.
- If the two answers are genuinely similar, the BODY is the problem. The skill is not changing behavior, so the base model was already doing what it says.

## When the body is weak

The skill states the obvious, or repeats what a capable model already does. Fix it by adding what the base model actually skips:

- A concrete, non-obvious step (the debugger's "reproduce before you fix", not "debug carefully").
- A decision or refusal the base model would not make on its own (refuse to ship without a test; delegate instead of guessing).
- A specific method, threshold, or ordering, not an adjective. "Rank findings P0 to P3 by user harm" beats "be thorough".

Do not pad the body with hedging prose to chase the rubric. A longer skill that says nothing new will not move the number, and it bloats the library.

## When the rubric is coarse

The rubric is too few items, or too easy, or tests presence instead of quality. Fix it by making it a HARDER, more discriminating test, never an easier one:

- Add items that capture the skill's real added value (for ship: "confirms a rollback path before deploying", "verifies production after deploy", not just "tags the release").
- Replace a binary that both outputs miss or both pass with one that separates a great answer from an adequate one.
- Test the behavior, not the vocabulary. "Positions the customer as the hero" is better checked by "the first sentence is about the reader's problem, not the product" than by banning a word.

## The trap

Raising the score by weakening the rubric is gaming, and it is the one move that makes the whole scorecard worthless. If a rubric change makes the eval easier, it is wrong even if the number goes up. The test is: after the change, would a mediocre answer still fail? If not, you loosened it. Tighten instead.

## If neither moves it

Some cases are at the ceiling: the base model is already excellent and the skill genuinely adds little for that task. That is a real finding. Record it and move on. Not every skill needs to win every case; the library needs to be honest about where it does and does not add value.

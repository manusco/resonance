# Active Recall: predict-then-reveal, and when to bother

> Reading builds recognition; prediction builds recall. The check-in turns a passive explainer into retained understanding, but only when the material is worth keeping.

## When retention is worth the work

Offer a check-in when the reader will need this again: a concept the codebase now depends on, a change they will build on, a decision they will defend. Skip it for a throwaway fix or a one-time context dump. A forced check-in on trivial material trains the reader to skip check-ins.

## Predict-then-reveal (for a change)

The strongest shape for a diff, a bug, or a behavior. The order is the whole technique:

1. Show only the raw change: the diff, the input, the failing case, the setup. Nothing about the outcome or the reason.
2. Ask one specific question: what will this do, why did it break, what will the output be.
3. End the turn. The reader answers before seeing anything else.
4. Only after the prediction lands, reveal the explanation, and point directly at where the reader's model matched or diverged.

The hard rule, restated because it is the one always violated: never put the answer, a hint, or the explanation in the same message as the question. A prediction made against a visible answer is recognition, not recall. If you cannot bear to end the turn without explaining, you are optimizing for looking helpful over the reader learning.

## Checked exercise (for a concept)

When there is no single change to predict, pose a small problem that applies the concept: "given this input, what would the new validator reject?" Let the reader work it, then confirm or correct. Same ordering rule: the problem and the answer never share a message.

## Correcting a wrong prediction

A wrong prediction is the point of the exercise, not a failure. Show exactly where the reader's model diverged from reality, in the reader's own terms. The gap between what they expected and what happened is where the learning is; name it precisely and do not paper over it.

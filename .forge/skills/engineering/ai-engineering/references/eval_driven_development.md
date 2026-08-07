# Eval-Driven Development

> "You cannot ship what you cannot measure. You can only demo it."

An eval is a test for a non-deterministic system. It turns "the prompt feels better now" into "the pass rate went from 71% to 88%". Without it, every prompt change is a gamble and every regression is invisible until a user finds it.

## Contents
- Why evals come first
- The three grader types
- Building the golden set
- LLM-as-judge
- The regression gate
- Common mistakes

## 1. Why Evals Come First

The order is not "build the feature, then test it". The order is:

1. Collect real inputs (or write plausible ones).
2. Define what a good output is (the rubric).
3. Build the harness that scores an output against the rubric.
4. Only now, write the prompt and iterate against the number.

If you write the prompt first, you will tune it to the three examples in your head and it will break on the fourth. The eval set is the specification. A feature with no eval has no definition of correct.

## 2. The Three Grader Types

Pick the cheapest grader that can actually detect the failure you care about.

| Grader | Scores | Use for | Cost |
| :--- | :--- | :--- | :--- |
| **Exact / structural** | Deterministic checks: valid JSON, contains the ID, matches regex, correct enum | Extraction, classification, format compliance | Free |
| **Model-graded (judge)** | A model scores the output against a rubric (relevance, faithfulness, tone) | Summaries, answers, open-ended text | Cheap, noisy |
| **Human-graded** | A person rates it | The 20 cases that decide launch; calibrating the judge | Expensive |

Layer them. Structural checks catch the cheap failures for free. The judge handles subjective quality. Humans calibrate the judge and settle the cases that matter.

## 3. Building The Golden Set

- **Size**: 20 to 50 cases to start. Enough to catch real variance, small enough to run often. Grow it as bugs surface.
- **Source**: real user inputs beat invented ones. Mine logs. Every production failure becomes a new eval case so it can never regress silently.
- **Coverage**: happy path, the boring middle, the adversarial edge, and the inputs that must be refused. A set of only easy cases proves nothing.
- **Freeze it**: the golden set is version-controlled and stable. If you change a case, you are changing the spec, and you say so.
- **Label the expected behavior, not the exact string**: for open text, grade against a rubric ("mentions the refund window, does not invent a policy"), not against one blessed answer.

## 4. LLM-As-Judge

A model grading another model's output. Powerful, and easy to do badly.

- **Give it a rubric, not a vibe**: "Score 1 if the answer is fully supported by the provided context, 0 if any claim is not." Not "is this good?".
- **Prefer binary or low-cardinality scores**: a judge distinguishing 1 to 10 is mostly noise. Pass/fail, or a 3-point scale, is more stable.
- **Show it the reference**: give the judge the retrieved context or the gold answer to compare against. Judging in a vacuum measures fluency, not correctness.
- **Calibrate against humans**: sample 20 judge verdicts, have a human check them. If the judge disagrees with humans, fix the judge prompt before trusting the number. Raw agreement flatters on a mostly-pass set: a judge that says pass to everything scores 90 percent on a set that is 90 percent good and catches nothing, so check two things separately, does it agree with humans and does it catch the cases you already know are bad.
- **Know the noise floor before you trust a delta**: run the unchanged system through the eval twice. The spread between the two runs is measurement noise, the smallest change you can actually detect. A score that moves less than that spread has not moved. Binary scores and a frozen set are what keep the floor low enough for real change to show.
- **Position and verbosity bias are real**: judges favor the first option and the longer answer. Randomize order in pairwise comparisons.

## 5. The Regression Gate

The eval is worthless if you do not act on it.

- Every prompt change, model swap, or retrieval-setting change runs the full golden set.
- A drop on the golden set blocks the change. No "I'll fix it later".
- Track the number over time. A prompt that fixes case 12 and breaks case 30 is not progress.
- Run it in CI where the host supports it, so no change merges without a passing set.

## 6. Common Mistakes

- **Testing on the examples you tuned on**: circular. Hold out cases the prompt has never seen.
- **One giant subjective score**: "quality: 7/10" tells you nothing about what broke. Score specific dimensions: faithfulness, completeness, format.
- **Grading fluency instead of correctness**: a smooth, confident, wrong answer must fail. Make sure the grader catches it.
- **Never growing the set**: if production keeps surprising you, your set is too small or too clean. Feed failures back in.
- **Skipping the eval because "it's obviously better"**: that is exactly the belief evals exist to check.

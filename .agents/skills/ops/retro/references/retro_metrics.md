# Retro Metrics: exact definitions, computed from git

> A retro metric you cannot compute the same way twice is a vibe, not a metric. Each metric below has one definition and the git command that produces it, so two people (or two agents) get the same number from the same history.

## Contents

- Shipping Streak
- Focus Score
- Complexity Delta
- Test Ratio
- Reading the numbers

## Shipping Streak

Consecutive calendar days, ending today, that have at least one commit.

```
git log --since="30 days ago" --format=%ad --date=short | sort -u
```

Count back from today: the streak is the run of consecutive dates present with no gap. A gap of one day resets it. This measures cadence, not volume; one honest commit a day beats a Friday dump.

## Focus Score

The share of commits that stayed inside one area of the codebase, versus commits that sprayed across many. A focused commit touches files under a single top-level directory; a scattered one spans three or more.

```
git log --since="7 days ago" --name-only --format="C:%H"
```

For each commit, take the set of top-level directories of its changed files. Classify: 1 top-level dir is focused, 2 is mixed, 3 or more is scattered. Focus Score is `focused / total`, a fraction from 0 to 1. A low score means the week was context-switching, which is the hidden drag a feelings-based retro misses.

## Complexity Delta

Net lines over the window, and whether the code grew faster than it was pruned.

```
git log --since="7 days ago" --numstat --format=""
```

Sum insertions (column 1) and deletions (column 2). Complexity Delta is `insertions - deletions`. Report it next to new capability: a large positive delta with little new user-facing behavior is complexity accreting. A negative delta on a week that still shipped features is healthy pruning. The number is not good or bad on its own; it is good or bad relative to what was delivered.

## Test Ratio

Lines of test code changed versus lines of application code changed.

```
git log --since="7 days ago" --numstat --format=""
```

Partition changed files into test paths (matching `test`, `spec`, `__tests__`, `.test.`, `.spec.`) and the rest. Test Ratio is `test_lines_changed / app_lines_changed`. It is a coverage-of-effort signal, not coverage of lines: a week of application code with zero test lines is a flag, whatever the coverage report says.

## Reading the numbers

- No single metric is a verdict. Focus Score plus Complexity Delta plus what shipped tells a story; any one alone misleads.
- These measure the system and the code, never a person's worth. A scattered week is usually a planning failure, not a discipline failure.
- The core question the numbers serve is one thing: are we moving faster this week than last, at the same or better quality.

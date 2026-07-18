# The KPI Tree: one north-star, decomposed into drivers

> A company does not have forty metrics. It has one number that matters and a tree of drivers that feed it. The tree turns a wall of dashboards into a claim: move these drivers, and the north-star moves. If your metrics do not form a tree, you are measuring, not steering.

## Contents

- [1. Why a Tree, Not a Dashboard](#1-why-a-tree-not-a-dashboard)
- [2. Choosing the North-Star](#2-choosing-the-north-star)
- [3. Decomposing Into Drivers](#3-decomposing-into-drivers)
- [4. Leading vs Lagging](#4-leading-vs-lagging)
- [5. The Tree Is Made of met- Entries](#5-the-tree-is-made-of-met-entries)
- [6. The Company Scorecard](#6-the-company-scorecard)
- [7. Worked Example](#7-worked-example)
- [8. Failure Modes](#8-failure-modes)

## 1. Why a Tree, Not a Dashboard

A dashboard is a pile of numbers with no stated relationship. It tells you what is happening and not what to do. A tree states the relationship: the north-star at the root, and under it the two to four drivers that mathematically produce it, each decomposed again until you reach a metric an owner can move this week.

The tree is a hypothesis about how the business works. "Revenue is driven by new customers and retention; new customers is traffic times conversion; retention is activation times ongoing value." That is a claim you can be wrong about, which is what makes it useful. When the north-star moves and you cannot say which driver moved it, the tree is incomplete and the next review should fix the tree before it chases the number.

## 2. Choosing the North-Star

The north-star is the one metric that best captures the value customers get from the product, expressed so that it rises only when the business is genuinely healthier. For most companies it is a recurring-value number: monthly recurring revenue, weekly active teams, activated accounts. It is rarely raw signups and never cumulative anything.

Two tests for a candidate north-star:

- **The value test.** Does it go up only when customers are getting more value. Signups pass this test only if signups reliably become value, which they usually do not.
- **The reversibility test.** Can it go down. A north-star that can only rise (total registered users, lifetime signups) measures the past, not the present. If a bad month cannot move it, it cannot steer.

One north-star. A company with three north-stars has none, because when they conflict, and they will, nothing says which wins.

## 3. Decomposing Into Drivers

Break the north-star into the factors that multiply or sum to produce it, then break those again. Stop when you reach a metric a single owner can move with a single week's work.

The decomposition is arithmetic, not vibes. New MRR equals new customers times average price. New customers equals qualified traffic times signup conversion times paid conversion. Each node is literally the product or sum of its children, so when a child moves you can predict the parent. A "driver" that does not arithmetically connect to its parent is a metric you happen to like, not part of the tree.

Depth of three or four levels is usually enough. Past that, the leaves get so small that moving one does nothing measurable to the root, and the tree stops earning its complexity.

## 4. Leading vs Lagging

Every node is either leading or lagging, and a working tree pairs them.

- **Lagging** metrics confirm the outcome after it is set: revenue, churn, closed deals. They are true and they are late. You cannot act on a lagging metric; by the time it moves, the quarter that produced it is over.
- **Leading** metrics predict the lagging ones early enough to change them: trial activations this week, demos booked, product usage depth. They are noisier and they are actionable.

The discipline: manage the leading metrics, grade on the lagging ones. A review that watches only revenue is always driving by the rear-view mirror. A review that watches only leading metrics can fool itself with activity that never converts. Pair each lagging node with the leading node that is supposed to move it, and check the link is real: if activations keep rising and revenue stays flat, the assumed link is broken, and that is the finding.

## 5. The Tree Is Made of met- Entries

Each node is a `met-` entry in `.resonance/ledger/metrics.md`, appended over time. A reading is never an edit; it is a new entry, so the history of the node is intact and trends are real.

```
## met-mrr-2026-07: MRR, July 2026
type: metric
created: 2026-08-01
status: closed
value: 42000
unit: eur
target: 50000
as_of: 2026-07-31
source: stripe dashboard, manual pull
```

The tree structure lives in this reference and in the scorecard the review reads; the ledger holds the readings. A node with a `target` and a `due:` date is also a live key result (see the OKR cascade). One record, two uses: the KPI tree reads it as a driver, the OKR cascade reads it as a graded outcome.

## 6. The Company Scorecard

The scorecard is the tree rendered for the weekly review: north-star at the top, drivers indented beneath, each showing current value, target, and last-week trend. It is generated from the `met-` entries, not maintained by hand, so it can never disagree with the ledger.

Reading the scorecard top to bottom is the first step of the weekly business review. A red north-star sends you down its branches to find the driver that broke. A green north-star with a red driver underneath is a warning the good number is about to turn. The tree is what lets a single read of the board tell you not just that something is wrong, but where.

## 7. Worked Example

A B2B SaaS north-star of MRR decomposes like this:

```
MRR (north-star, lagging)
  New MRR (lagging)
    New customers (lagging)
      Qualified traffic (leading)
      Signup conversion (leading)
      Trial-to-paid conversion (leading)
    Average new price (leading)
  Retained MRR (lagging)
    Gross retention (lagging)
      Activation rate (leading)
      Feature adoption depth (leading)
    Net expansion (leading)
```

Every leaf is something an owner moves in a week: run a conversion experiment, tighten the trial nudge, ship the activation step. Every branch is arithmetic, so a moved leaf has a predictable effect on the root. When MRR misses, you do not guess. You walk the branch that fell short and land on the leaf that stalled.

## 8. Failure Modes

- **A dashboard, not a tree.** Metrics with no stated relationship. If you cannot say which driver moves the root, build the tree first.
- **Multiple north-stars.** Three top metrics that conflict under pressure. Pick one.
- **Vanity root.** Cumulative signups or total users as the north-star. It only rises, so it cannot steer.
- **All lagging.** A tree of outcomes with no leading indicators. You will always find out too late.
- **Disconnected drivers.** Nodes that do not arithmetically produce their parent. A metric you like is not a driver.
- **Hand-kept scorecard.** A board maintained separately from the ledger, so the two drift and every review argues about which is right.

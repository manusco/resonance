# Paid Unit Economics: CAC, LTV:CAC, ROAS, Payback, Scaling Rules

> The arithmetic that decides whether spend compounds or leaks. Every scaling decision passes through this file first. If the economics do not clear, no targeting trick saves the account.

## Contents
- The metrics, defined
- The CAC ceiling
- LTV:CAC and payback
- ROAS and its trap
- Blended vs channel economics
- Scaling rules
- When to hold or cut
- Unit economics checklist

## The metrics, defined

- **CAC (customer acquisition cost)**: total spend to acquire one paying customer. Include media plus the fees that scale with it. Cost per lead is not CAC; divide spend by customers, not by clicks or leads.
- **LTV (lifetime value)**: gross-margin value a customer delivers over their lifetime, not revenue. Use contribution margin, not top-line. A high-revenue, low-margin customer can still lose money.
- **ROAS (return on ad spend)**: revenue divided by ad spend for a period. A ratio (4:1) or a multiple (4x). Fast to read, easy to misread (see the trap below).
- **Payback period**: months to recover CAC from a customer's margin. This is the cash-flow constraint. A profitable LTV with a 14-month payback can still bankrupt a business that cannot float 14 months of spend.

## The CAC ceiling

Before scaling anything, know the most the business can pay to acquire a customer and stay profitable. That ceiling is set by margin and payback tolerance, not by the platform.

- Derive it from contribution margin and how long the cash position can wait for payback.
- A channel that beats its own CTR benchmark but sits above the CAC ceiling is a losing channel. Kill it or fix the economics.
- Every channel is judged against this one number.

## LTV:CAC and payback

- Working target for most businesses: **LTV:CAC of 3:1 or better**. Below roughly 3:1, thin margin leaves nothing for overhead and error. Well above it may mean underspending, room to scale exists.
- Payback should fit the cash position. Consumer and low-ticket: often weeks to a few months. B2B and high-ticket: longer paybacks are survivable because contract value is larger and retention is stronger.
- Use both. A great ratio with an unsurvivable payback is still a cash-flow problem.

## ROAS and its trap

ROAS is revenue-based, so it hides margin. 4:1 ROAS on a 20% margin product loses money; 2:1 on a 70% margin product prints it. Convert ROAS to a margin view before trusting it.

- Break-even ROAS = 1 / gross margin. A 25% margin needs 4:1 just to break even on the media, before any overhead.
- Prefer contribution-margin and payback framing for scaling decisions. Keep ROAS as a fast directional read, not the verdict.

## Blended vs channel economics

- **Channel CAC**: cost within one channel. Use it to decide which channels to scale, hold, or cut.
- **Blended CAC**: total sales-and-marketing spend divided by all new customers, including the ones organic and word of mouth would have delivered anyway. Use it as the honest business-level number.
- The gap matters. A paid channel can look efficient on a last-click view while mostly harvesting demand other efforts created. Watch blended CAC to catch a channel that is taking credit, not creating customers.

## Scaling rules

Scale winners without resetting the algorithm's learning.

- **Confirm first**: only scale a channel or campaign whose economics clear the CAC ceiling with payback the business can survive. Scaling a loser loses money faster.
- **Step, do not jump**: raise budget in increments the learning phase can absorb, not a single large jump that throws the campaign back into re-learning and spikes cost. Give each step time and volume to stabilize before the next.
- **Split the budget**: keep most spend on proven winners, a slice on structured tests against winning audiences, a small slice on genuine new bets (new platform, angle, format).
- **Watch marginal, not average**: as you scale, the next dollar costs more than the last. When the marginal CAC crosses the ceiling, you have found the efficient frontier for that channel. Stop there and open a new channel rather than forcing spend past the point it stays profitable.

## When to hold or cut

- **Hold** when economics are marginal but improving, or when a test has not reached significance. Do not scale on hope; do not cut on one bad week.
- **Cut** when a channel sits above the CAC ceiling after a fair test and a real optimization pass. More budget will not fix broken economics.
- **Stop and fix upstream** when every channel loses money: the problem is the product, offer, price, or funnel, not the media. Paid amplifies the offer; it does not rescue a bad one.

## Unit economics checklist

- [ ] CAC ceiling derived from margin and payback tolerance, written down before scaling.
- [ ] LTV computed on contribution margin, not revenue.
- [ ] LTV:CAC at or above the working target; payback fits the cash position.
- [ ] ROAS converted to a margin view (break-even ROAS = 1 / gross margin) before trusting it.
- [ ] Blended CAC checked against channel CAC to catch channels taking undue credit.
- [ ] Scaling done in steps that respect the learning phase, watching marginal CAC.
- [ ] Losing channels cut or fixed upstream, not fed more budget.

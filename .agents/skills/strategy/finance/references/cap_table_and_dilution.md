# Cap Table and Dilution

> Dilution is priced ownership, not loss. The only question is whether the capital buys more value than the slice it costs.

## Contents

- [1. What a Cap Table Is](#1-what-a-cap-table-is)
- [2. Pre-Money, Post-Money, and Ownership](#2-pre-money-post-money-and-ownership)
- [3. Dilution Across Rounds](#3-dilution-across-rounds)
- [4. The Option Pool Shuffle](#4-the-option-pool-shuffle)
- [5. SAFEs and Convertible Notes](#5-safes-and-convertible-notes)
- [6. Pro-Rata and Following On](#6-pro-rata-and-following-on)
- [7. A Few Term-Sheet Mechanics](#7-a-few-term-sheet-mechanics)
- [8. Cap Table Failure Modes](#8-cap-table-failure-modes)

## 1. What a Cap Table Is

A capitalization table is the ledger of who owns what. Founders, employees (via the option pool), and investors, each with a number of shares and a percentage of the total. It is arithmetic, not mystique, and every founder should be able to run it themselves.

The number that matters is not shares, it is percentage of the fully diluted total: all shares that exist or could exist if every option and convertible were exercised. Ownership is always measured on the fully diluted basis, because that is what you actually own after everything converts.

This reference covers the math so you can model outcomes and sanity-check what a lawyer drafts. The legal terms of any financing are for a qualified startup lawyer; model the ownership, hand the paperwork to counsel.

## 2. Pre-Money, Post-Money, and Ownership

The single most important mechanic, and the one founders most often get backward.

- **Pre-money valuation**: what the company is worth before the new investment.
- **Post-money valuation**: pre-money plus the amount raised.
- **Investor ownership**: their check divided by the post-money, not the pre-money.

```
Post-money = Pre-money + Amount raised
New investor ownership % = Amount raised / Post-money
Dilution to existing holders % = Amount raised / Post-money
```

Worked example: you raise 2M on an 8M pre-money valuation.

```
Post-money        = 8M + 2M      = 10M
Investor owns     = 2M / 10M     = 20%
Everyone existing = diluted by     20%
```

If founders held 100 percent before, they now hold 80 percent. The existing holders keep the same number of shares; new shares are issued to the investor, so everyone's slice of the larger pie shrinks proportionally. Dilution is the price of the pie getting bigger, not shares taken from you.

## 3. Dilution Across Rounds

Dilution compounds across rounds. Each round dilutes everyone who came before, including investors from prior rounds. Founders should model the full arc, not one round in isolation, because the ownership at exit is what matters.

A simplified multi-round arc (illustrative, not typical targets):

```
Start:        Founders 100%
Seed:         sell 20%  -> Founders 80%
Series A:     sell 25%  -> Founders 80% x 75% = 60%
Series B:     sell 20%  -> Founders 60% x 80% = 48%
```

Each round multiplies the retained fraction, it does not subtract. Selling 20 percent then 25 percent then 20 percent does not leave you with 35 percent; it leaves you with 100% x 0.80 x 0.75 x 0.80 = 48 percent. Modeling this early keeps founders from waking up under-owning their own company after three rounds.

The lesson is not "avoid dilution". It is "each round of dilution should buy a milestone that raises the value of your remaining, smaller stake by more than the slice you sold". Owning 48 percent of a company worth 100M beats owning 100 percent of a company worth 2M. Dilution done right makes your smaller slice worth far more in absolute terms.

## 4. The Option Pool Shuffle

The most common way founders get diluted more than they realize.

The option pool is shares set aside for future employees. Investors almost always require a pool (often 10 to 20 percent) to be in place before their money goes in. The catch: the pool is typically carved out of the pre-money valuation, which means it dilutes the founders and existing holders, not the new investor.

```
Without pool in pre-money:  investor 20%, founders 80%
With 15% pool in pre-money: investor 20%, pool 15%, founders 65%
```

The pool "shuffle" is that a bigger pre-money pool looks generous to future employees but comes entirely out of the founders' slice while leaving the investor's ownership untouched. Two defenses:
- **Size the pool to the actual hiring plan**, not a round number the investor proposes. If you will hire three people before the next round, you do not need a 20 percent pool.
- **Negotiate whether the pool comes from pre- or post-money.** Pre-money pool = founders pay for it. Post-money pool = everyone shares it. This is a real negotiable, not a fixed rule.

## 5. SAFEs and Convertible Notes

Early rounds often use instruments that postpone setting a valuation until a later priced round. Two common ones:

- **SAFE (Simple Agreement for Future Equity):** the investor gives cash now for the right to shares in the next priced round. Not debt, no interest, no maturity date.
- **Convertible note:** similar, but structured as debt: it carries interest and a maturity date, and converts to equity at the next round.

Both usually carry two terms that reward the early investor for taking early risk:

- **Valuation cap:** the maximum valuation at which their money converts. If the next round prices higher than the cap, they convert at the cap, getting more shares for their money. The cap protects the early investor's upside.
- **Discount:** a percentage (often 10 to 20 percent) off the next round's price. They convert cheaper than the new investors.

The mechanic to watch: **SAFEs and notes dilute you when they convert, not when you sign them.** A stack of uncapped or low-cap SAFEs raised casually before a priced round can convert into far more ownership than expected, because the conversion math only becomes visible at the priced round. Model the conversion of every outstanding SAFE and note into your pre-round cap table before you agree the priced round, or the fully diluted ownership will surprise you at the worst moment. "We raised a bit on SAFEs" is how founders accidentally give away 30 percent before their first priced round.

## 6. Pro-Rata and Following On

Pro-rata is an existing investor's right to buy enough of the next round to maintain their ownership percentage. Without exercising it, they get diluted like everyone else.

- **Why it matters to investors:** their biggest returns come from doubling down on winners. Pro-rata lets them keep their percentage in the companies that are working. Strong investors care a lot about this right.
- **Why it matters to founders:** pro-rata rights held by early investors consume part of each new round, leaving less room for new investors. Usually fine and often welcome (it is a vote of confidence), but worth modeling so the round has room for the new lead you want.

## 7. A Few Term-Sheet Mechanics

Ownership percentage is not the whole story. A few terms change who gets what in an exit, and they are why founders retain a lawyer. The math founders should understand:

- **Liquidation preference:** who gets paid first in an exit and how much before common shares (founders and employees) see anything. A "1x non-participating" preference means the investor takes the larger of their money back or their ownership percentage. Participating or multiple preferences can mean investors take a disproportionate share of a modest exit, so a high headline valuation with an aggressive preference can be worth less to founders than a lower valuation with clean terms.
- **Vesting:** founder and employee shares typically vest over time (commonly four years with a one-year cliff), so leaving early forfeits unvested shares. This protects the team and the company against a co-founder walking away with a large stake for little work.
- **Anti-dilution:** protects investors if a later round prices below theirs (a down round) by adjusting their conversion, at the founders' expense. Standard, but the specific form matters.

The point of listing these is not to negotiate them from this reference. It is to know they exist and can matter more than the valuation number, so you model the economics and let counsel handle the terms.

## 8. Cap Table Failure Modes

- **Confusing pre- and post-money.** Computing ownership off pre-money instead of post-money, understating the dilution. The most common arithmetic error.
- **Ignoring the option pool shuffle.** Accepting a large pre-money pool without realizing it comes entirely from the founders' slice.
- **SAFE stacking.** Raising round after round on uncapped or low-cap SAFEs and only discovering the total dilution when they all convert at the priced round.
- **One-round tunnel vision.** Optimizing a single round's dilution without modeling the full arc to exit, then under-owning the company after three rounds.
- **Chasing valuation over terms.** Taking the highest valuation with an aggressive liquidation preference, when a lower valuation with clean terms leaves founders better off in most exit scenarios.
- **Messy cap table.** Undocumented handshake equity promises and informal splits that become a legal mess and a diligence red flag at the next raise.

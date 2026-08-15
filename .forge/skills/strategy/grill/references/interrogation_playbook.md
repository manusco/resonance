# Interrogation Playbook

The question banks for a grill session, ordered by dependency. Resolve upper branches before lower ones, because the answers upstream constrain the questions downstream. Pull one question at a time from the branch you are on. Skip any question the codebase already answers.

## Walk order

1. Intent and problem
2. Scope boundary
3. Data and contracts
4. State and lifecycle
5. Failure and edge cases
6. Done-criteria and rollout

Do not run this as a linear script. Follow the answers. When an answer invalidates something upstream, walk back before going deeper.

## 1. Intent and problem

- What is the expensive problem this solves? If we shipped nothing, what breaks and for whom?
- Who feels the pain today, and how do they work around it now?
- Why now, and why this shape rather than the obvious alternative?

## 2. Scope boundary

- What is explicitly out of scope for this pass? Name it so it stops being ambiguous.
- What is the smallest version that is still worth shipping?
- Is this a one-way door (hard to reverse) or a two-way door? One-way doors earn more questions.

## 3. Data and contracts

- What is the shape of the core entity? What fields, what types, what is optional?
- Where does the data come from, where does it live, who else reads or writes it?
- What is the interface this exposes and what does it consume? What contract must not break?
- What already exists in the repo that this should reuse rather than reinvent?

## 4. State and lifecycle

- What are the states this thing moves through, and what triggers each transition?
- What are the empty, loading, error, and success states? Design the shadow states before the happy path.
- What is idempotent and what is not? What happens on a retry or a double submit?

## 5. Failure and edge cases

Run the failure lens on each resolved area and keep the ones that matter:

- Zero and scale: behavior at 0 items and at 10,000 items.
- Mobile and offline: the small screen, the dropped network, the slow connection.
- Concurrency: two users, one record, at the same moment.
- Hostile input: malformed, oversized, or adversarial data at the boundary.
- Permission: the wrong user, the expired session, the missing role.

## Targeted risk pass

Run this pass only when the plan earns it:

- one-way door;
- security or privacy boundary;
- money, billing, legal, or compliance exposure;
- migration, data-loss, or rollback risk;
- broad blast radius;
- missing critical fact.

Pick one to three relevant checks. Do not simulate a panel. Report:

- strongest objection;
- missing evidence;
- required contract or plan change;
- whether an independent decision review is needed.

## 6. Done-criteria and rollout

- How do we know it works? Name the observable, checkable outcome, not "it works".
- What is the test that would fail today and pass when this is done?
- How does this ship: behind a flag, to everyone, migrated in place? What is the rollback?
- What do we measure after launch to know it did the job?

## The recommendation rule

Every question above is asked with your recommended answer attached and one concrete reason. The user reacts to a proposal, they do not author from a blank prompt. If you cannot form a recommendation, that gap is itself the thing to surface.

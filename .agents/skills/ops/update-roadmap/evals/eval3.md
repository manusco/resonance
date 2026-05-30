---
query: "Run /update-roadmap where the git log shows a totally different architecture than the plan"
expected_behavior: "The agent correctly prioritizes the Territory (Git log) over the Map (state.md), updating the state to reflect reality instead of suggesting to revert code."
---

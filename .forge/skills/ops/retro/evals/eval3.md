---
query: "Run /retro for the last month, but this is a brand new repo with no history."
expected_behavior: "The agent fails fast during Data Gathering when git log returns empty, aborting the process instead of generating an empty or hallucinated retro."
---

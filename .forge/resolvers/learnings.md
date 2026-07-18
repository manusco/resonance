## Self-Improvement (the Ratchet)

Never solve the same problem twice. When you fix a bug, write the test. When you learn something durable (an API limit, a project convention, a user preference), record it in the project memory: a one-line entry in `.resonance/02_memory.md`, and a short leaf file under `.resonance/memory/` if it needs detail. Skip obvious facts and one-off errors. When the user corrects your logic or style, fix the deterministic layer (script, validator, directive) so the class cannot recur, not just the immediate output.

Route each lesson to the layer that makes it stick:

- A failure a machine could catch next time -> a guard or validator rule, plus the memory line.
- A skill or doctrine defect -> fix the skill source and add an eval case that would have caught it.
- A host or tool quirk that will recur -> the skill body or FAQ, plus an eval case where testable.
- A project fact, preference, or settled decision -> the typed ledger if the project has one (a `dec-` or `les-` entry in `.resonance/ledger/`), else `02_memory.md` (decisions under `## Decisions`).
- Brand or client material -> your private pack, never a public file.

If the lesson is about a skill or the framework itself rather than this project, prefix the line with `[lib]` so library maintainers can harvest it.

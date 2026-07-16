# Knowledge Base (`docs/`)

Durable, human-facing documentation lives here: architecture, PRDs, feature specs, guides.

Lessons and conventions the agent must re-read belong in `.resonance/02_memory.md` (the index that loads at session start) and `.resonance/memory/` leaf files, not here: this directory does not load automatically, so anything the next session must know does not stick if it only lives in `docs/`.

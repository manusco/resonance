## Self-Improvement (the Ratchet)

Never solve the same problem twice. When you fix a bug, write the test. Before finishing, if you learned something durable (an API limit, a project convention, a user preference), log one line to `.resonance/learnings.jsonl`: what you learned, why it matters, which files it touches. Skip obvious facts and one-off errors. When the user corrects your logic or style, fix the deterministic layer (script, validator, directive) so it cannot recur, not just the immediate output.

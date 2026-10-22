# Installation simplification plan

## Outcome
Every new installation includes the complete framework runtime and authoring tools. Existing source and compiled manifests continue to update without profile prompts, while preserving project files and locally modified framework files.

## Scope
The updater, consumer health check, focused updater/consumer tests, and this plan. Legacy profile labels remain accepted as inputs; updates normalize to the complete source profile. Verified installed release provenance may authorize updating previously owned files. Newly included files are written only when absent or already equal to the incoming bytes. Unclaimed collisions remain project-owned. Existing Git-backed transaction recovery remains in place.

## Verification
Reproduce a compiled consumer missing a helper required by bundled skills. Then verify a complete installation can execute runtime helpers, source/compiled legacy upgrades need no profile choice, unrelated files and unverified collisions survive, and failed updates recover from Git without a redundant backup tree.

# Field reports and correction proposals

The field-report path turns a sanitized observation into two review proposals: a lesson block and an eval stub marked `needs-eval`. It does not append to the ledger, change a skill, run or promote an eval, open a review queue, or schedule the delayed outcome. The operator and repository maintainer still perform those steps.

## Capture a safe report

Use the public GitHub issue form only for content that is safe to publish. Remove secrets, personal information, customer data, private project details, provider URLs, and raw traces. Prefer a short opaque run ID that is safe to publish. Never paste a restricted report into a public issue and label it restricted. The `restricted-do-not-submit` option is a warning and a record of intent, not a GitHub submission control.

An existing local JSON report can omit all new metadata and remains valid. The normalized report shape is:

```json
{
  "skill": "resonance-ops-qa",
  "id": "qa-missed-empty",
  "summary": "the empty-state case was not tested",
  "scenario": "A sanitized list view with zero items rendered no empty state.",
  "expected": ["show the empty state", "add a regression test"],
  "run_id": "run-8f21",
  "artifact_version": "v2.5.41",
  "sensitivity": "public-sanitized",
  "owner_role": "skill-maintainer",
  "outcome": "the empty-state regression passes in the next release",
  "due_date": "2026-11-10"
}
```

The GitHub form does not feed this CLI automatically. Normalize an issue into JSON manually: copy the skill and summary, turn the expected behavior into a JSON string array, copy the sanitized scenario, and omit blank optional answers. The `host` answer is context for a human reviewer and is not copied by the converter.

Attribution is optional, but `run_id` and `artifact_version` must appear together. They are submitter-provided and remain unverified by this tool. `owner_role` may stand alone for an immediate correction. A delayed `outcome` requires both `due_date` and `owner_role`; `outcome` and `due_date` must appear together. The role is a lowercase slug, not a person's name. The due date must be a real `YYYY-MM-DD` date. Keep each field short and public-safe.

`sensitivity` may be `public-sanitized` or `restricted-do-not-submit`. This is a submitter's declaration, not a privacy scan or a verified classification. The converter does not detect secrets, personal information, customer data, or private project details. Restricted reports are refused before proposal output or `--eval-out` writes. Keep restricted source records in an adopter-controlled private store; redact a derivative first, inspect it, then submit that derivative as `public-sanitized`. Legacy reports without a sensitivity field continue to parse; their safety depends on the operator following the former instruction to remove private details before conversion.

## Generate and review proposals

```sh
py .forge/field_report.py --file report.json
py .forge/field_report.py --file report.json --eval-out /path/outside-the-repo/review/05_field_regression.json
```

The first command prints the proposed lesson and eval stub. The second also writes the stub to the explicitly selected path. The path must be outside active `.forge/skills/**/evals/` and `.agents/skills/**/evals/` directories because the eval runner loads every JSON file there, including `needs-eval` stubs. Keep the proposal outside the repository until accepted. Check the output for accidental disclosures before sharing it. The report metadata is copied into the proposal as unverified provenance; do not treat a run ID as proof of identity or bind it to private traces without a host's access controls.

The human correction lifecycle is:

1. **Triage:** a maintainer checks that the report is reproducible, public-safe, and in the right skill's scope. They may reject it or request safer/more evidence outside this CLI.
2. **Decide:** an accountable artifact owner decides whether the lesson and regression proposal reflect the intended behavior. A role slug in the report is a routing hint, not an assignment, authenticated identity, or approval.
3. **Propose:** the maintainer edits the lesson and eval stub, removes unsupported claims, and keeps the eval in `needs-eval` until its case and assertions are reviewed. The lesson output is prose, not a ledger entry: after acceptance, add the ledger-required `status`, `confidence`, and `review_due` fields before appending it. An accountable role may be recorded for an immediate correction without a delayed outcome. If an outcome is supplied, both a due date and owner role are required.
4. **Verify:** run the relevant skill/library checks and evals; require an independent reviewer for consequential changes. Passing a generated stub alone is not evidence of skill lift.
5. **Apply:** merge or distribute a reviewed change through the adopter's ordinary release path. Where an adapter supports production changes, that adopter defines a bounded canary, approval receipt, observation window, and tested rollback to the prior artifact/version.
6. **Check outcome:** the adopter's accountable owner checks the stated outcome on or after `due_date` and records the observed result in the adopter's system of record. This CLI does not create a reminder or close the loop.

Rejected reports and unaccepted proposals must not change the canonical skill. No step silently promotes a skill or reduces human review.

## Host adapter and privacy boundary

The public issue form and this converter are a manual fallback, not a connected correction service. They do not authenticate the reporter, verify the run/artifact relationship, protect an issue from public access, route to a named steward, or enforce the permissions of a host.

A future adapter must keep restricted traces and customer data in an access-controlled private store; emit a sanitized report to the shared review surface; bind authenticated actor, run ID, host, skill/workflow version or digest, and trace to that private record; and provide an authorization-checked review decision with actor, scope, and timestamp. It must prove that rejection leaves artifacts unchanged and acceptance still requires normal tests and human approval. If it changes running behavior, it must demonstrate rollback. The adopter chooses and staffs the human steward and the artifact owner; Resonance does not ship a queue, identity provider, production binding, scheduler, canary controller, or rollback service.

See [the architecture boundary](ARCHITECTURE_BOUNDARY.md) for adapter conformance evidence and the distinction between declared policy and enforced permissions.

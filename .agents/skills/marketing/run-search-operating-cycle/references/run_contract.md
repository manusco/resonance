# Search Run Contract

Create a JSON contract before collecting or interpreting evidence.

## Required fields

```json
{
  "property_registry": [
    {"property_id": "public-site", "property_uri": "sc-domain:example.org", "owner_role": "SEO owner"}
  ],
  "cadence": "monthly",
  "timezone": "Europe/Berlin",
  "credential_reference": "secret-manager:gsc-readonly",
  "artifact_destination": {"kind": "private", "path": "/private/work/search-runs"},
  "comparison_window": {"current_start": "2026-07-01", "current_end": "2026-07-31", "prior_start": "2026-06-01", "prior_end": "2026-06-30"},
  "previous_run": "private:search-runs/2026-06"
}
```

Rules:

- `property_registry` is the scoped set. Each entry uses a stable public or operational identifier and an owner role. Do not record a person's name or email.
- `cadence` records the intended comparison rhythm. It is not authorization to schedule anything.
- `timezone` controls date boundaries and must be explicit.
- `credential_reference` points to an existing credential. It never contains the credential value.
- `artifact_destination.kind` defaults to `private`. A `repository` destination requires `repository_write_approved: true`, an exact path, and redacted content.
- `comparison_window` contains explicit inclusive dates. Do not silently compare unequal windows.
- `previous_run` is a reference or `null` for the first run. It must not embed prior raw data.

Run `python3 scripts/validate_search_run.py contract.json` before evidence collection.

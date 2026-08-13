# Automated Scanning Protocol

Automated scanning is a filter, not a verdict. Use it to find review targets, enforce known safety rules, and catch regression classes that humans should not rediscover by hand.

## 1. Scope First

Name the scope before running tools:

- working tree,
- staged changes,
- branch diff,
- full repository,
- package or service slice,
- infrastructure or deployment config.

A failed build, dirty tree, or missing dependency is audit context. It should not erase the audit unless the requested check cannot run at all.

## 2. Scan Stack

Use the cheapest signal that can answer the question.

| Layer | Finds | Gate |
| :--- | :--- | :--- |
| Dependency scan | Known vulnerable packages, abandoned libraries, malicious package risk | Block high-confidence critical or exploited issues. |
| Secret scan | Keys, tokens, certificates, private URLs, sensitive config | Block any live secret or credible credential pattern. |
| Static analysis | Dangerous APIs, taint paths, auth gaps, unsafe framework use | Block high-confidence paths. Queue noisy rules for review. |
| Container scan | OS package CVEs, root images, stale base layers | Block reachable critical issues in shipped images. |
| Infrastructure scan | Public ingress, wildcard IAM, missing encryption, weak network policy | Block exposed sensitive assets and privilege escalation. |
| Dynamic scan | Runtime auth, headers, redirect, XSS, SSRF, rate-limit behavior | Block reproducible production-relevant exploit paths. |
| Agentic review | Hard-to-rank candidates across large codebases | Block only after evidence and revalidation. |

## 3. Candidate Lifecycle

Every scoped target needs an outcome:

- **clean**: checked and no material candidate remains,
- **candidate**: suspicious signal exists, but exploitability is not proven,
- **finding**: input, path, missing guard, impact, and fix are clear,
- **rejected**: signal was reviewed and does not hold,
- **fixed**: finding was revalidated after a change,
- **skipped**: target was intentionally excluded with reason,
- **incomplete**: target could not be checked.

Do not approve when coverage is unknown. Unknown coverage is an audit finding about the review itself.

## 4. Evidence Standard

A scanner finding needs:

- affected file, symbol, route, resource, or config,
- attacker-controlled input or unsafe trigger,
- vulnerable path to sink or policy failure,
- missing or insufficient guard,
- affected asset and user harm,
- confidence and severity as separate fields,
- reproduction or deterministic check where possible,
- fix direction and verification command.

Never file raw scanner output as a final security finding.

## 5. False Positive Control

Alert fatigue is a security bug.

- Separate blocking gates from review queues.
- Disable or refine repeated low-value rules.
- Require owners, reasons, and expiry dates for suppressions.
- Keep positive and negative fixtures for custom rules.
- Remove stale candidates when file content, rule version, or config changes.
- Make full scans and diff scans follow the same invalidation rules.

## 6. CI Trust Boundary

Untrusted code should not receive secrets or broad write access.

- Run change analysis without production credentials.
- Freeze dependency installs where possible.
- Pin third-party actions.
- Prefer OIDC or short-lived credentials for publishing jobs.
- Keep privileged reporting in a separate job that consumes a constrained artifact.
- Log whether credentials are configured, never their values or partial fingerprints.

## 7. Stop Conditions

Stop the line when evidence shows a credible path to:

- exposed production secrets,
- auth bypass,
- remote code execution,
- injection into a privileged data store,
- public access to private data,
- privilege escalation across tenant or role boundaries,
- critical dependency exposure with a reachable runtime path.

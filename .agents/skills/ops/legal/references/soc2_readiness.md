# SOC2 Readiness

SOC2 is an attestation report on how well a company protects customer data, produced by an independent auditor (a CPA firm) against the AICPA Trust Services Criteria. Enterprise buyers ask for it. It is not a law and not a certification you pass once; it is an ongoing evidence discipline. This reference covers what SOC2 is, the readiness process, and how it relates to GDPR.

## Contents
- What SOC2 is and is not
- Type I vs Type II
- The Trust Services Criteria
- The readiness gap process
- Evidence collection
- SOC2 vs GDPR
- Checklist

## What SOC2 is and is not

- **Is**: an independent auditor's report describing your controls over security (and optionally availability, confidentiality, processing integrity, privacy) and whether they were designed and operated effectively.
- **Is not**: a legal requirement, a certificate you hang on the wall, or a substitute for GDPR compliance. It is a sales enabler and a forcing function for security hygiene.

The report goes to your customers and their auditors under NDA. Its value is trust: it lets an enterprise buy from you without running their own full security review.

## Type I vs Type II

- **Type I**: controls are suitably **designed** at a point in time. Faster and cheaper. A snapshot. Useful as a first milestone.
- **Type II**: controls **operated effectively over a period** (commonly 3 to 12 months). This is what serious buyers want, because it proves the controls actually run, not just that they exist on paper.

Sequence for most startups: get to readiness, do a Type I to unblock early enterprise deals, then run the observation window and do a Type II.

## The Trust Services Criteria

SOC2 is built on five criteria categories. **Security (the Common Criteria) is mandatory**; the other four are optional and chosen based on what you promise customers:

1. **Security**: protection against unauthorized access. Access control, change management, risk assessment, monitoring, incident response. Always in scope.
2. **Availability**: the system is available per commitments. Relevant if you offer an uptime SLA.
3. **Confidentiality**: confidential information is protected. Relevant if you handle sensitive business data.
4. **Processing Integrity**: processing is complete, accurate, timely, authorized. Relevant for systems where correct processing is the product (payments, data pipelines).
5. **Privacy**: personal information is handled per your notice and criteria. Overlaps with, but does not equal, GDPR.

Scope only what you can support with evidence. Adding Availability means committing to uptime monitoring and evidence you may not yet have.

## The readiness gap process

Readiness is the work before the audit. The steps:

1. **Define scope**: which criteria, which systems and products, which environments.
2. **Gap assessment**: compare current controls against the criteria. Where is there no policy, no evidence, or a broken process?
3. **Write the policies**: SOC2 expects documented policies (access control, change management, incident response, vendor management, business continuity, data classification). Policies must be real and followed, not shelfware.
4. **Implement the controls**: close the gaps. Enforce MFA, least-privilege access, logging, change approvals, onboarding/offboarding, background checks, vendor reviews.
5. **Operate and collect evidence**: run the controls and capture proof over the observation window (for Type II).
6. **Pick an auditor and undergo the audit.**

The technical implementation of many controls (encryption, audit logging, access control, monitoring) is `resonance-ops-security`'s domain. This skill owns the program: scope, policies, evidence discipline, and auditor readiness.

## Evidence collection

SOC2 is an evidence exercise. Auditors want proof that controls operated, not assurances. Typical evidence:

- Access reviews (who has access to what, reviewed on a schedule).
- Onboarding and offboarding records (access granted and revoked promptly).
- Change management logs (code changes reviewed and approved before deploy).
- MFA enforcement across systems.
- Vulnerability scans and remediation records.
- Incident response records and postmortems.
- Vendor risk reviews (including that your sub-processors have their own controls).
- Backup and recovery tests.
- Security-awareness training completion.

The practical failure is scrambling for evidence at audit time. Instrument evidence collection continuously; compliance-automation platforms exist for exactly this, but the discipline matters more than the tool.

## SOC2 vs GDPR

They overlap but are different things, and neither replaces the other:

- **SOC2** is a voluntary, auditor-attested report on controls, driven by US enterprise sales expectations. Framework-based.
- **GDPR** is binding EU law with fines, driven by regulators and data-subject rights. Law-based.

A SOC2 report does not make you GDPR compliant, and GDPR compliance does not produce a SOC2 report. A company selling to EU enterprises often needs both: SOC2 to close the deal, GDPR because it is the law. The security controls overlap heavily (access control, encryption, monitoring), so the work compounds; the legal obligations do not.

## Checklist

- [ ] Scope defined: which criteria (Security mandatory) and which systems.
- [ ] Gap assessment done against the chosen criteria.
- [ ] Required policies written and actually followed.
- [ ] Controls implemented (MFA, least privilege, change management, logging, vendor reviews).
- [ ] Evidence collection running continuously, not assembled at audit time.
- [ ] Type I vs Type II decision made against the sales timeline.
- [ ] Auditor (CPA firm) selected.
- [ ] Understood that SOC2 does not equal GDPR; both handled where both apply.

Escalation: the audit itself is done by a licensed CPA firm, which is the required external party. Legal counsel should review the security commitments you make to customers (in the ToS, MSA, and DPA) so your contractual promises match what SOC2 actually attests, and so you do not over-commit to controls you cannot evidence.

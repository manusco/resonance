# Privacy Policy

A privacy policy is a truthful, plain-language description of what personal data you process and why. Under GDPR it is how you satisfy the transparency duty (Articles 13 and 14). It is a mirror of your real data flows, not a document you buy. A policy that does not match reality is a signed admission of non-compliance.

## Contents
- The rule: build from the data map
- Mandatory disclosures
- Structure that works
- Boilerplate traps
- DACH specifics
- Drafting checklist

## The rule: build from the data map

You cannot write the policy before you know the data flows. Get the data map first (see gdpr_dach_privacy for the full model): for each category of personal data, what is collected, the purpose, the lawful basis, where it is stored, how long, and every third party it goes to. The policy is then a readable rendering of that map. If you find yourself writing a sentence you cannot trace to a real flow, stop and either fix the map or cut the sentence.

## Mandatory disclosures

GDPR Article 13 (data collected from the person) and Article 14 (data obtained elsewhere) require, at minimum:

- **Who you are**: the controller's identity and contact details. For a German-market site, this ties to the Impressum.
- **DPO contact** if you have appointed one.
- **What you collect and why**: each purpose of processing.
- **Lawful basis** for each purpose. If you rely on legitimate interests, state the interest.
- **Recipients**: the categories or names of third parties the data is shared with (processors, analytics, payment, hosting).
- **International transfers**: whether data leaves the EU/EEA and the safeguard used (adequacy, SCCs).
- **Retention**: how long each category is kept, or the criteria used to decide.
- **Data-subject rights**: access, rectification, erasure, restriction, portability, objection, and the right to withdraw consent where consent is the basis.
- **Right to complain** to a supervisory authority.
- **Source** of the data, if not collected from the person (Article 14 cases).
- **Automated decision-making / profiling**, if any, with meaningful information about the logic.

## Structure that works

Ordinary readers and regulators both benefit from a predictable layout:

1. Controller identity and contact (and DPO, if any).
2. What data you collect, grouped by source: provided by the user, collected automatically (logs, cookies), received from third parties.
3. Purposes and lawful basis, ideally as a table mapping purpose to data category to basis to retention.
4. Cookies and tracking (or a link to a dedicated cookie notice) with the consent mechanism.
5. Who you share data with (processors and their function) and international transfers.
6. Retention periods.
7. Data-subject rights and how to exercise them, including the DSAR route.
8. Right to complain to a supervisory authority.
9. Changes to the policy and effective date.

Keep it in plain language. A layered notice (a short summary up top, full detail below) satisfies transparency better than a wall of legalese.

## Boilerplate traps

The failure mode is copying another company's policy. Concretely, that produces:

- **Named data you do not collect** (a scraped policy mentioning payment card data when you use Stripe and never touch card numbers) which misstates your processing.
- **Omitted processors you do use**: your actual analytics, email, and hosting vendors are missing, so the recipient disclosure is false.
- **Wrong lawful bases**: the template says "consent" for everything, but your billing runs on contract and your security logging on legitimate interests.
- **Missing retention periods** because the template left them blank.
- **A US-centric template** ("we comply with CCPA") pasted onto an EU business, missing GDPR's actual requirements.
- **Placeholder text left in**: "[Company Name]" or "insert jurisdiction" shipped to production.

Every one of these is discoverable by a regulator or a plaintiff and turns the policy from a shield into evidence.

## DACH specifics

- German market: the notice is the Datenschutzerklärung and is expected in German. Pair it with a compliant Impressum (contact, legal form, register number, VAT ID where applicable) under the DDG. Missing or wrong details are a frequent Abmahnung trigger.
- Cookies and non-essential tracking need prior consent (TDDDG in Germany), so the cookie banner must actually block scripts until consent, not just display a notice.
- Switzerland: a Swiss-facing notice should also address the revDSG; if you serve both EU and CH users, the policy must satisfy both.

## Drafting checklist

- [ ] Data map exists and is current; every policy line traces to it.
- [ ] Controller identity and contact present.
- [ ] Each purpose has a stated lawful basis.
- [ ] Legitimate-interest purposes name the interest.
- [ ] All real processors and their functions are disclosed.
- [ ] International transfers and their safeguard are stated.
- [ ] Retention period given per category.
- [ ] All data-subject rights listed, with a working DSAR route.
- [ ] Right to complain to a supervisory authority included.
- [ ] Cookie/tracking consent mechanism described and actually enforced.
- [ ] No placeholder text, no named data you do not collect, no US-only framing.
- [ ] Effective date and a note on how changes are communicated.

Escalation: a founder can reach draft quality here. Have a lawyer review before publishing if you process special-category data, run profiling or automated decisions, transfer data internationally without an obvious mechanism, or operate in a regulated sector (health, finance, children's data).

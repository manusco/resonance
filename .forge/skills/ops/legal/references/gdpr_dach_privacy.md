# GDPR and DACH Data Protection

The first-principles model of EU data protection, with the Germany, Austria, and Switzerland specifics a founder actually hits. GDPR territorial scope is not "any EU user, anywhere, for any reason." Article 3 applies when processing is in the context of an EU establishment, or when a non-EU controller or processor offers goods or services to people in the EU, monitors their behavior in the EU, or is in a place where Member State law applies by public international law.

## Source Card

- Primary source: https://eur-lex.europa.eu/eli/reg/2016/679/art_3/oj
- Secondary source: https://www.edpb.europa.eu/documents/guideline/guidelines-32018-on-the-territorial-scope-of-the-gdpr-article-3-version-adopted_en
- Verified: 2026-08-15
- Scope: GDPR Article 3 territorial scope.
- Review trigger: EDPB territorial-scope guidance update, new adequacy decision, or cross-border data-flow recommendation.

## Contents
- Core definitions
- The six lawful bases
- The seven processing principles
- Data-subject rights and DSAR handling
- Controller vs processor
- EU data residency and international transfers
- DACH specifics: DE, AT, CH
- Common founder mistakes

## Core definitions

- **Personal data**: any information relating to an identified or identifiable person. Includes name, email, IP address, cookie IDs, device IDs, location. Broader than most founders assume.
- **Special category data**: health, biometric, genetic, racial or ethnic origin, political opinions, religion, trade-union membership, sex life or orientation. Processing is prohibited by default and needs a specific Article 9 exception.
- **Processing**: any operation on personal data: collecting, storing, using, sharing, deleting. Doing almost anything with the data is processing.
- **Controller**: decides the why and how. **Processor**: acts only on the controller's instructions.

## The six lawful bases

Every processing purpose needs exactly one lawful basis (GDPR Article 6). Choose the honest one per purpose, do not default to consent.

1. **Consent**: freely given, specific, informed, unambiguous, and as easy to withdraw as to give. No pre-ticked boxes. No bundling ("agree to everything to use the app"). Weak for anything you need to run the business, because withdrawal must be frictionless.
2. **Contract**: processing necessary to deliver a service the person asked for. Billing a paying user, shipping their order. The strongest basis for core product function.
3. **Legal obligation**: a law requires it. Keeping invoices for tax retention.
4. **Vital interests**: to protect someone's life. Rare outside health and emergency contexts.
5. **Public task**: exercising official authority. Mostly public bodies.
6. **Legitimate interests**: a real business interest not overridden by the person's rights. Requires a documented balancing test (the LIA: purpose, necessity, balancing). Common for fraud prevention, network security, basic analytics. Not available to public authorities for their tasks.

Marketing note: unsolicited electronic marketing is governed by ePrivacy and national laws, not only GDPR. In DACH, cold B2C email is generally consent-required, and German B2B cold email is high-risk under UWG unless a narrow exception applies. Do not promise that cold email is fine; require jurisdiction, recipient type, source of contact data, consent or existing-customer basis, unsubscribe handling, and counsel review for risky sends.

## The seven processing principles

GDPR Article 5 sets the principles every controller must satisfy and be able to demonstrate (accountability):

1. **Lawfulness, fairness, transparency**: have a basis, do not deceive, tell people what you do.
2. **Purpose limitation**: collect for a specified purpose, do not silently repurpose.
3. **Data minimization**: collect only what the purpose needs. The single most violated principle. If a form field is not used, delete it.
4. **Accuracy**: keep data correct and current; fix or erase what is wrong.
5. **Storage limitation**: keep it only as long as needed, then delete. Define a retention period per data category.
6. **Integrity and confidentiality**: secure the data (encryption, access control). The security build is `resonance-ops-security`; the obligation is here.
7. **Accountability**: be able to prove all of the above. This is why the data map and the Article 30 record of processing exist.

## Data-subject rights and DSAR handling

People have enforceable rights over their data. A Data Subject Access Request (DSAR) is any exercise of them.

- **Access** (Art. 15): a copy of their data and the processing details.
- **Rectification** (Art. 16): correct inaccurate data.
- **Erasure / "right to be forgotten"** (Art. 17): delete, subject to exceptions (a legal retention duty can override).
- **Restriction** (Art. 18): pause processing while a dispute is resolved.
- **Portability** (Art. 20): export in a machine-readable format, for consent- or contract-based processing.
- **Objection** (Art. 21): stop processing based on legitimate interests; for direct marketing the objection is absolute.
- **Rights around automated decisions** (Art. 22): not to be subject to solely automated decisions with legal or similar significant effect, with safeguards.

Handling rules: respond within one month (extendable by two more for complexity, with notice). Verify identity before disclosing. Usually free; a manifestly unfounded or excessive request can be charged or refused, with reasons. Build a route (email or in-product) to receive and log these; the ability to fulfill an erasure or export request is a system-design requirement, not an afterthought.

## Controller vs processor

The role sets the duties. A B2B SaaS is typically both at once:

- **Processor** for the personal data its customers put into the product (the customer's end users). Duties: act only on the customer's documented instructions, sign a DPA with each customer, keep the data secure, help the customer meet DSARs, not engage sub-processors without permission, and not repurpose the data.
- **Controller** for its own data: employees, prospects, website visitors, the billing contact at each customer. Duties: lawful basis, transparency (privacy policy), honor data-subject rights, keep the Article 30 record.

Getting the role wrong cascades: a processor that starts using customer data for its own model training has silently become a controller for that use and needs its own lawful basis and transparency, which it almost never has. Flag any such repurposing.

## EU data residency and international transfers

Personal data can move freely inside the EU/EEA. Sending it outside needs a transfer mechanism (GDPR Chapter V):

- **Adequacy decision**: the destination country is deemed adequate by the European Commission (for example the UK, Switzerland, and, for certified US organizations, the EU-US Data Privacy Framework). No extra safeguard needed for covered transfers.
- **Standard Contractual Clauses (SCCs)**: the common fallback. The EU-approved clauses, plus a transfer impact assessment on the destination's surveillance laws, plus supplementary measures where needed.
- **Binding Corporate Rules**: for intra-group transfers in large organizations. Heavy to set up.

Practical founder reality: using US cloud vendors (AWS, Google, common SaaS) means transfers. Many offer EU regions and SCCs; choosing an EU region and signing the vendor's DPA with SCCs covers most cases. International transfers are a frequent escalation point: get counsel to confirm the mechanism before relying on it.

## DACH specifics: DE, AT, CH

GDPR is the floor; each country layers on.

- **Germany (DE)**: the Bundesdatenschutzgesetz (BDSG) supplements GDPR, notably on employee data and the duty to appoint a **Datenschutzbeauftragter (DPO)**. A company generally must appoint a DPO once at least 20 people are constantly engaged in automated processing of personal data (a lower, Germany-specific threshold than the GDPR default). Enforcement is by the state data-protection authorities (per Bundesland). Website tracking and cookies also fall under the TDDDG (successor to TTDSG), which requires prior consent for non-essential cookies.
- **Austria (AT)**: the Datenschutzgesetz (DSG) supplements GDPR; the regulator is the Datenschutzbehörde (DSB). Broadly aligned with GDPR, with local procedural specifics.
- **Switzerland (CH)**: not in the EU/EEA. The revised Federal Act on Data Protection (revDSG, the nFADP, in force since September 2023) is GDPR-aligned but a separate law. Switzerland has an EU adequacy decision, so EU-to-CH transfers are covered; a Swiss company serving EU users still falls under GDPR for those users and must satisfy both. The regulator is the FDPIC (EDÖB).

Language note: DACH users expect the privacy notice (Datenschutzerklärung) and often an Impressum in German. A German-market site typically needs a legally compliant Impressum under the DDG (formerly TMG); missing or wrong Impressum details are a common ground for Abmahnung (formal warning letters).

## Common founder mistakes

- Treating consent as the universal basis when contract or legitimate interests is the honest fit, then being unable to function when someone withdraws.
- A privacy policy copied from another company that names data flows the business does not have and omits ones it does.
- No retention periods, so data is kept forever, violating storage limitation.
- Collecting form fields "just in case," violating data minimization.
- Assuming a US SaaS vendor is fine with no thought to the transfer mechanism.
- No way to actually fulfill an erasure or export request, so a DSAR cannot be honored within the deadline.
- Ignoring the German cookie-consent and Impressum duties, inviting an Abmahnung.

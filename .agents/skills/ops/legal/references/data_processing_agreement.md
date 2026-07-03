# Data Processing Agreement (DPA)

A Data Processing Agreement is the contract GDPR requires whenever one party processes personal data on another's behalf. It is mandated by Article 28. If your SaaS handles your customers' user data, you need a DPA with those customers; if you use vendors that touch personal data, you need a DPA with each vendor. No DPA where one is required is itself a breach.

## Contents
- When a DPA is required
- The controller / processor / sub-processor chain
- Article 28 mandatory terms
- The sub-processor position
- Practical patterns
- Checklist

## When a DPA is required

A DPA is required whenever a **processor** handles personal data on behalf of a **controller**. Apply the test from gdpr_dach_privacy:

- Your customer decides why and how their end-users' data is processed and puts that data into your product. They are the controller; you are the processor. You need a DPA where you are the processor and they are the controller.
- You use a hosting, email, analytics, or support vendor that stores or accesses that personal data. That vendor is your sub-processor. You (now acting as the controller's processor) need a DPA with the vendor.

No DPA is needed for data where you are the sole controller and no one processes it for you (for example, purely internal data you host yourself). But the moment a third party touches personal data on your instruction, the obligation triggers.

## The controller / processor / sub-processor chain

Data flows down a chain, and DPAs sit on every link:

- **Controller** (your customer) → **Processor** (you) → **Sub-processor** (your vendors: AWS, an email provider, a support tool).

Each link needs a DPA that passes the controller's protections down. The controller's obligations must flow through you to your sub-processors, so your sub-processor DPAs cannot offer weaker protection than what you promised the controller.

## Article 28 mandatory terms

A valid DPA must include, at minimum:

1. **Subject matter, duration, nature, and purpose** of the processing, plus the types of personal data and categories of data subjects. Usually an annex.
2. **Process only on documented instructions** from the controller, including for international transfers, unless required by law (then notify, unless the law forbids it).
3. **Confidentiality**: persons authorized to process are bound to confidentiality.
4. **Security**: appropriate technical and organizational measures (Article 32). Often an annex listing encryption, access control, backups.
5. **Sub-processors**: the processor engages none without the controller's prior authorization (specific or general with notice of changes and a right to object), and imposes the same data-protection terms by contract.
6. **Assist the controller** in responding to data-subject rights requests.
7. **Assist the controller** with security, breach notification, data protection impact assessments, and prior consultation.
8. **Deletion or return** of all personal data at the end of the service, and deletion of copies, unless law requires retention.
9. **Make available** the information needed to demonstrate compliance, and allow and contribute to audits and inspections by the controller or its auditor.

A DPA missing any of these is not Article 28 compliant, no matter what it is titled.

## The sub-processor position

Two models, and the choice is a real business decision:

- **Specific authorization**: the controller approves each sub-processor by name. Higher trust, but operationally heavy: you must go back for approval every time you add a vendor.
- **General authorization with notice**: the controller pre-approves your use of sub-processors, you maintain a public list, and you notify of changes with a window for the controller to object. This is the standard SaaS pattern. Keep the sub-processor list current and honest; it is a promise, and adding a vendor you did not disclose breaks it.

Where sub-processing crosses borders (a US cloud region), the transfer mechanism (SCCs, adequacy) must be in place on that link too. This is a frequent escalation point.

## Practical patterns

- **You are the SaaS (processor)**: publish a DPA that customers can accept, ideally as part of your terms or via a signed addendum. Enterprise customers will often push their own DPA; be ready to review it (that becomes a contract review).
- **You use vendors (they are sub-processors)**: sign each vendor's DPA. Reputable vendors offer one. If a vendor that touches personal data has no DPA, that is a red flag: either get one or do not send them personal data.
- **Annexes carry the detail**: the data categories, the security measures, and the sub-processor list live in annexes. Keep them accurate rather than aspirational.

## Checklist

- [ ] Roles correctly identified: who is controller, processor, sub-processor for this data.
- [ ] A DPA exists on every link where a party processes personal data for another.
- [ ] All nine Article 28 terms are present.
- [ ] Sub-processor model chosen (specific or general with notice) and the list is current.
- [ ] Security-measures annex reflects what you actually do, not a wish list.
- [ ] International-transfer mechanism attached where any link crosses the EU/EEA border.
- [ ] End-of-service deletion/return term present.
- [ ] Data-category and data-subject annex filled in for the real data.

Escalation: reviewing an enterprise customer's bespoke DPA, or setting up international-transfer mechanisms (SCCs plus transfer impact assessment), should go to counsel. A founder can accept a standard vendor DPA and publish a standard customer DPA, but a heavily negotiated one carries real liability and needs a lawyer's read.

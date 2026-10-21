# Business skill eval coverage audit, 2026-10-21

This audit covers marketing, sales, market research, finance, leadership, hiring, and customer success. The committed baseline is 96 cases across 22 skills. I reviewed each committed case against its skill template and the linked references used by the scenario. The domain contains 134 cases after this change, with every suite at six or more. I added 38 cases. Outbound sequence has seven because its existing privacy/deliverability case and two separate missing failure modes, opt-out suppression and conflicting source evidence, test distinct behavior.

No model eval runs were performed, so this report makes no score or lift claim. Checks here are static JSON parsing, required-field/count validation, and diff review. The new cases use scenario-specific observable outcomes and allow equivalent safe alternatives where appropriate.

## Marketing

| Skill | Cases before → after | Existing cases reviewed and retained |
|---|---:|---|
| analytics | 5 → 6 | `01_measurement_plan`, `02_low_traffic_significance`, `03_last_click_budget_cut`, `04_planted_defect`, `05_content_learning_loop`: decision-to-event design, power and peeking, attribution limits, dishonest experiment claims, and the boundary between measurement and creative ownership. All are grounded in distinct prompts; the short learning-loop rubric is specific to what impressions/likes cannot establish. |
| content-distribution | 5 → 6 | `01_organic_channel_plan`, `02_ambiguous_routing`, `03_video_packaging`, `04_planted_defect`, `05_stale_specs`: repurposing, specialist routing, video packaging, engagement manipulation, and volatile platform facts. The cases exercise different workflow steps. |
| conversion | 6 → 6 | `01_cro_audit`, `02_trust_verification`, `03_offer_problem`, `04_planted_defect`, `05_commercial_vs_product_actions`, `06_rate_without_page_evidence`: evidence limits, claim trust, offer diagnosis, product-claim mismatch, distinct commercial/product action hierarchies, and missing page evidence. Retained because each scenario tests a separate decision boundary. |
| copywriter | 7 → 7 | `01_happy_path`, `02_humanization`, `03_trust_integrity`, `04_longform_argument`, `05_planted_defect`, `05_rhetorical_tells`, `06_channel_strategy_boundary`: hero copy, evidence-bounded rewriting, unsupported metrics, long-form argument, banned phrasing, style variation, and ownership routing. `02_humanization` was corrected after review: it requests only the rewrite, so its global banned-word check no longer conflicts with a required diagnosis quoting those words; arbitrary short-sentence quotas were removed. The duplicate `05_` filename stem is pre-existing; both files remain canonical and distinct. |
| lifecycle | 5 → 6 | `01_onboarding_activation`, `02_long_time_to_value`, `03_batch_spray_and_dark_pattern`, `04_planted_defect`, `05_newsletter_boundary`: activation, naturally delayed value, batch/dark-pattern rejection, involuntary churn, and newsletter ownership. The newsletter boundary is intentionally separate from lifecycle system design. |
| paid-acquisition | 4 → 6 | `01_b2b_saas_program`, `02_tiny_budget`, `03_scale_unprofitable`, `04_planted_defect`: unit economics, low-budget allocation, scaling unprofitable spend, and ad-to-page message match. Added pacing anomaly and attributed-ROAS incrementality gaps. |
| run-campaign | 3 → 6 | `01_happy_path`, `02_planted_defect`, `03_scope_boundary`: cross-specialist orchestration, DACH outreach compliance, and scope routing. Added missing brief inputs, outcome attribution handoff, and unverified campaign claims. |
| run-search-operating-cycle | 6 → 6 | `01_happy_path`, `02_missing_contract`, `03_cannibalization_grain`, `04_repository_write_gate`, `05_truncated_evidence`, `06_no_scheduling`: run contract, paired-dimension evidence, write authorization, incomplete exports, and scheduling boundary. The brief missing-contract rubrics remain specific to exact fields and the pre-evidence gate. |
| seo | 5 → 6 | `01_striking_distance`, `02_geo_citation`, `03_thin_content`, `04_planted_defect`, `05_experimental_machine_signals`: ranking opportunity, citation claims, thin content, unsupported external claims, and emerging machine-readable signals. Added a parameterized URL crawl/index tradeoff case. |

Added cases: analytics `06_tracking_breakage`; content distribution `06_source_permission_boundary`; lifecycle `06_suppression_and_reentry`; paid acquisition `05_budget_pacing_shock` and `06_incrementality_claim`; campaign `04_no_outcome_definition`, `05_measurement_handoff`, and `06_campaign_asset_claim`; SEO `06_crawl_budget_tradeoff`.

## Sales

| Skill | Cases before → after | Existing cases reviewed and retained |
|---|---:|---|
| account-intelligence | 4 → 6 | `01_happy_path`, `02_no_fabricated_urgency`, `03_sparse_data_brief`, `04_planted_defect`: signal-based ranking, no fabricated urgency, evidence gaps, and customer-safe deck content. Added stale/conflicting signals and sensitive personal data boundaries. |
| call-intelligence | 4 → 6 | `01_discovery_calls`, `02_single_transcript`, `03_mixed_speakers`, `04_planted_defect`: multi-call synthesis, low-confidence single-call analysis, speaker inference, and exact-quote integrity. Added partial/noisy transcript limits and embedded transcript instructions (separate cases). |
| cold-call | 4 → 6 | `01_happy_path`, `02_no_proof_point`, `03_highly_skeptical_persona`, `04_planted_defect`: basic structure, absent proof, skeptical buyer adaptation, and pressure/fake-scarcity refusal. Added unverified product-claim handling and consumer/jurisdiction scope boundary. |
| lead-ops | 4 → 6 | `01_treatment_audit`, `02_owner_provenance`, `03_no_auto_escalation`, `04_planted_defect`: lead treatment, ownership evidence, approval for escalation, and new-cycle SLA integrity. Added duplicate/opt-out handling and timezone/calendar ambiguity in SLA measurement. |
| outbound-sequence | 5 → 7 | `01_happy_path`, `02_no_fabricated_proof`, `03_no_auto_send`, `04_planted_defect`, `05_privacy_deliverability`: source-backed sequence design, proof integrity, send gate, zero-signal mass outreach, fake reply framing, surveillance language, and deliverability. Retained all five. Added explicit opt-out suppression and stale/conflicting personalization evidence as two distinct gaps. |
| pipeline | 4 → 6 | `01_normal_pipeline`, `02_missing_dates`, `03_single_rep`, `04_planted_defect`: normal metrics, missing close dates, single-rep view, and forecast manipulation. The concise single-rep rubric matches its narrow structural edge case. Added mixed currency/duplicate rows and uncalibrated stage probability provenance. |
| revops | 4 → 6 | `01_capacity_and_coverage_plan`, `02_forecast_call_inspection`, `03_comp_plan_for_the_motion`, `04_planted_defect_forecast_inflation`: capacity math, evidence-based commit, incentive alignment, and forecast honesty. Kept quantified capacity rubric tied to provided assumptions; added thin-sample capacity and commit-incentive gaming boundaries. |
| run-revenue-motion | 3 → 6 | `01_pipeline_motion`, `02_compliance_risk`, `03_forecast_quality`: end-to-end routing and approval gates, scraped-contact compliance, and unweighted forecasting. The two short risk rubrics directly test separate explicit failure modes; they are not generic word-count fillers. Added contact-basis/opens boundary, missing customer handoff fields, and mixed-currency/fiscal-period forecast scope. |

Added cases: account intelligence `05_stale_signal_conflict`, `06_sensitive_account_data`; call intelligence `05_low_quality_transcript`, `06_transcript_prompt_injection`; cold call `05_jurisdiction_and_role_boundary`, `06_unknown_product_claims`; lead ops `05_duplicate_and_consent`, `06_sla_clock_boundary`; outbound sequence `06_objection_and_optout`, `07_source_conflict_personalization`; pipeline `05_currency_and_duplicate_rows`, `06_stage_probability_provenance`; RevOps `05_territory_capacity_conflict`, `06_incentive_gaming_boundary`; revenue motion `04_contact_basis_gate`, `05_customer_handoff_missing`, `06_forecast_scope_and_currency`.

## Research

| Skill | Cases before → after | Existing cases reviewed and retained |
|---|---:|---|
| market-research | 4 → 6 | `01_saas_category`, `02_traditional_industry`, `03_unproven_market`, `04_planted_defect`: actionable EDPs for a defined SaaS category, traditional-industry translation, uncertainty in emerging categories, and refusal to fabricate market statistics. Added conflicting category/source definitions and limits of a small friendly-customer sample. |

Added cases: `05_source_quality_conflict`, `06_customer_evidence_limit`.

## Finance, leadership, hiring, and customer success

| Skill | Cases before → after | Existing cases reviewed and retained |
|---|---:|---|
| finance/run-operating-cycle | 3 → 6 | `01_runway`, `02_unsourced_numbers`, `03_binding_action`: gross cash coverage versus net runway, unsourced actuals, and legal boundaries for financing terms. Added currency/accounting-basis reconciliation, scenario versus actual discipline, and investor-claim/action gates. |
| leadership/run-operating-cycle | 3 → 6 | `01_people_decision`, `02_legal_boundary`, `03_vague_operating_cycle`: people decisions with context, employment-risk boundaries, and converting vague goals to owners/cadence. Added unresolved decision rights, personnel confidentiality, and delegation/incident authority. |
| people/hiring | 4 → 6 | `01_happy_path`, `02_debrief_bias`, `03_comp_counteroffer`, `04_planted_defect`: full hiring loop, affinity/halo bias, comp-band decisions, and pressure to skip structured evaluation. Added retrospective rubric changes and fair, accessible work-sample design. |
| success/customer-success | 4 → 6 | `01_onboarding_to_value`, `02_health_and_renewal_forecast`, `03_expansion_and_nrr`, `04_planted_defect_discount_save`: first value, evidence-based health/forecast, expansion after value, and honest churn saves. Added unknown health evidence and unapproved roadmap commitments at renewal. |

Added cases: finance `04_fx_and_cash_basis`, `05_scenario_vs_actual`, `06_external_claim_and_action_gate`; leadership `04_decision_rights_conflict`, `05_confidential_people_context`, `06_delegation_without_authority`; hiring `05_late_rubric_change`, `06_work_sample_fairness`; customer success `05_missing_health_evidence`, `06_roadmap_commitment_boundary`.

## Limits

The evals are prompt fixtures, not production evidence. Source verification and platform/legal requirements still need current evidence at run time. None of these cases establishes measured improvement until the model-graded suites run in an isolated harness.

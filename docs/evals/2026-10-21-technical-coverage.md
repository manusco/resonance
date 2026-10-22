# Technical skill eval coverage audit

Date: 2026-10-21

Scope: canonical eval cases under `.forge/skills/{engineering,design,strategy,software}/**/evals/*.json` and their owning `skill.tmpl.md` files. I reviewed each baseline case against its query, expected behavior, and owning template contract. Existing cases were retained when their prompt exercised a distinct behavior, edge, failure, or authority boundary; the filename inventory below is the review index.

## Result

- Baseline: 138 cases across 25 skills, using Git HEAD as the starting count.
- Added: 23 distinct cases across 16 skills. All 25 technical skills now have at least six cases.
- After: 161 cases across 25 skills.
- No model-graded eval runs were executed, so this report makes no scored-lift claim.
- Structural validation is limited to JSON parsing, case-to-skill identity, required query/rubric shape, and minimum counts. Global eval gates remain with the coordinator.

## Per-skill review

| Skill | Before → after | Baseline cases reviewed | Added gap coverage |
|---|---:|---|---|
| `engineering/ai-engineering` | 4 → 6 | `01_new_llm_feature.json`, `02_rag_diagnosis.json`, `03_hallucination_and_cost.json`, `04_planted_defect.json` | `05_retrieved_instruction_injection.json`, `06_tool_failure_and_action_gate.json` |
| `engineering/automation` | 7 → 7 | `01_happy_path.json`, `02_mcp_server.json`, `03_sync_tool.json`, `04_planted_defect.json`, `05_early_measurement_bounded_unit.json`, `05_recurring_agent_loop.json`, `06_no_cut_quota_recovery.json` | None; existing cases cover distinct contracts for this skill. |
| `engineering/backend` | 5 → 6 | `01_happy_path.json`, `02_scope_creep.json`, `03_environment_resilience.json`, `04_planted_defect.json`, `05_type_evidence_erasure.json` | `06_retry_safe_webhook.json` |
| `engineering/build` | 8 → 8 | `01_case.json`, `02_case.json`, `03_case.json`, `04_planted_defect.json`, `05_implementation_selection.json`, `06_architecture_gate.json`, `07_architecture_gate_not_applicable.json`, `08_preserve_approved_workflow.json` | None; existing cases cover distinct contracts for this skill. |
| `engineering/database` | 4 → 6 | `01_safe_migration.json`, `02_query_optimization.json`, `03_engine_selection.json`, `04_planted_defect.json` | `05_large_table_backfill.json`, `06_tenant_data_integrity.json` |
| `engineering/debugger` | 4 → 6 | `01_flaky_bug.json`, `02_shotgun_fix.json`, `03_environment_bug.json`, `04_planted_defect.json` | `05_cannot_reproduce.json`, `06_agent_trajectory_failure.json` |
| `engineering/devops` | 6 → 6 | `01_cicd_pipeline.json`, `02_incident_response.json`, `03_environment_parity.json`, `04_planted_defect.json`, `05_validation_only_ci.json`, `06_queue_wait_vs_runtime.json` | None; existing cases cover distinct contracts for this skill. |
| `engineering/frontend` | 8 → 8 | `01_happy_path.json`, `02_cls_fix.json`, `03_shared_component.json`, `04_planted_defect.json`, `05_attention_path.json`, `06_motion_audit.json`, `07_task_first_workspace.json`, `08_form_scope_recovery.json` | None; existing cases cover distinct contracts for this skill. |
| `engineering/game-dev` | 4 → 6 | `01_core_loop.json`, `02_juice_injection.json`, `03_engine_selection.json`, `04_planted_defect.json` | `05_accessible_feedback.json`, `06_skill_and_fairness.json` |
| `engineering/mobile` | 6 → 6 | `01_offline_first.json`, `02_touch_physics.json`, `03_store_compliance.json`, `04_planted_defect.json`, `05_reach_and_motion_context.json`, `06_network_required_product.json` | None; existing cases cover distinct contracts for this skill. |
| `engineering/performance` | 5 → 6 | `01_measure_first.json`, `02_structural_vs_syntax.json`, `03_llm_finops.json`, `04_planted_defect.json`, `05_constraint_moves.json` | `06_tail_latency_and_quality.json` |
| `design/designer` | 10 → 10 | `01_happy_path.json`, `02_design_audit.json`, `03_shadow_states.json`, `04_register_and_slop.json`, `05_optical_craft_audit.json`, `06_cross_canvas.json`, `07_feel_special_refinement.json`, `08_planted_defect.json`, `09_daily_operations_queue.json`, `10_product_style_transfer.json` | None; existing cases cover distinct contracts for this skill. |
| `design/studio` | 5 → 6 | `01_happy_path.json`, `02_style_consistency.json`, `03_artifact_recovery.json`, `04_planted_defect.json`, `05_marketing_asset_brief.json` | `06_asset_rights_and_text.json` |
| `strategy/architect` | 5 → 6 | `01_happy_path.json`, `02_data_flow_audit.json`, `03_adr_stack_selection.json`, `04_planted_defect.json`, `05_boundary_evidence.json` | `06_ai_subsystem_boundary.json` |
| `strategy/blueprint` | 5 → 6 | `01_create_blueprint.json`, `02_conformance_check.json`, `03_brownfield_exception.json`, `04_planted_defect.json`, `05_missing_baseline.json` | `06_transition_conformance.json` |
| `strategy/brief` | 6 → 6 | `01_rough_request_route.json`, `02_clear_request_proportional.json`, `03_material_change_gate.json`, `04_untrusted_instructions.json`, `05_high_risk_external_action.json`, `06_exact_external_action.json` | None; existing cases cover distinct contracts for this skill. |
| `strategy/council` | 6 → 6 | `01_review_completed_analysis.json`, `02_high_risk_checkpoint.json`, `03_no_fake_independence.json`, `04_preserve_minority.json`, `05_simple_request.json`, `06_sensitive_context.json` | None; existing cases cover distinct contracts for this skill. |
| `strategy/finance` | 4 → 6 | `01_financial_model_runway.json`, `02_broken_unit_economics.json`, `03_prepare_raise.json`, `04_planted_defect.json` | `05_cohort_cac_attribution.json`, `06_missing_revenue_runway.json` |
| `strategy/grill` | 7 → 7 | `01_happy_path.json`, `02_codebase_first.json`, `03_too_simple_trap.json`, `04_planted_defect.json`, `05_low_risk_no_panel.json`, `06_high_risk_targeted_pass.json`, `07_no_fake_consensus.json` | None; existing cases cover distinct contracts for this skill. |
| `strategy/growth` | 5 → 6 | `01_retention_diagnosis.json`, `02_loop_design.json`, `03_flow_decay.json`, `04_planted_defect.json`, `05_content_distribution_boundary.json` | `06_incrementality_before_scale.json` |
| `strategy/gtm-thinker` | 4 → 6 | `01_campaign_review.json`, `02_positioning_shift.json`, `03_vague_concept.json`, `04_planted_defect.json` | `05_approved_campaign_boundary.json`, `06_hypothesis_rejected.json` |
| `strategy/plan` | 4 → 6 | `01_case.json`, `02_case.json`, `03_case.json`, `04_planted_defect.json` | `05_preserve_confirmed_contract.json`, `06_no_arbitrary_step_quota.json` |
| `strategy/researcher` | 7 → 7 | `01_happy_path.json`, `02_contradictory_sources.json`, `03_documentation_type.json`, `04_planted_defect.json`, `05_auth_crypto_existing_implementation.json`, `06_institutional_release_obligation.json`, `07_release_cost_decomposition.json` | None; existing cases cover distinct contracts for this skill. |
| `strategy/venture` | 4 → 6 | `01_happy_path.json`, `02_premature_build.json`, `03_pivot_or_persevere.json`, `04_planted_defect.json` | `05_pricing_test_evidence.json`, `06_vague_customer_segment.json` |
| `software/deliver-change` | 5 → 6 | `01_happy_path.json`, `02_one_way_door.json`, `03_planted_defect.json`, `04_scope_boundary.json`, `05_compatibility_delegation.json` | `06_ordinary_request_route.json` |

## Review findings and rubric repairs

- `strategy/plan/evals/01_case.json`: the old Dark Mode rubric forced both Researcher and Venture handoffs even though the owning template allows those only when unresolved evidence could change the choice or a business-model assumption is in scope. Reframed it as a settled local feature and now checks repository evidence, proportionate planning, relevant verification, and the approval boundary.
- `strategy/plan/evals/03_case.json`: expanded the two-item rubric to cover the missing scope, a focused clarification, no invented billing architecture, and no final plan before clarification.
- `strategy/venture/evals/01_happy_path.json`: corrected the interview-question count from three to five to match the owning Mom Test procedure.
- `strategy/gtm-thinker/evals/03_vague_concept.json`: corrected the typo `Hhalts` to `Halts`.
- `design/studio/evals/06_asset_rights_and_text.json`: scoped text/QR acceptance to approved copy and verified scan behavior; an image generator that can verify both remains acceptable. The case still protects customer consent, safe placement, and the distinction between asset creation and campaign approval.
- The other baseline rubrics were retained after review because their prompts own separate observable requirements. The newly added cases target named gaps such as retrieved-content injection, unknown webhook outcomes, resumable large-table backfills, non-reproducible reports, accessible game feedback, tail-latency regressions, approved asset rights, AI system boundaries, transition exceptions, cohort attribution, incrementality, rejected GTM hypotheses, and ordinary-language route boundaries.

## Limits

The cases are public authoring fixtures. No protected holdout, calibrated judge, live answerer, or comparative model run was used. The structural check can prove file integrity and contract shape only; it cannot prove model performance or invocation trajectories. A later scored run must use the approved operating contract, protected dataset, and separate qualified judge.

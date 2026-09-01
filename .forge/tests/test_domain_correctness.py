"""Regression tests for high-risk domain doctrine."""
import re
import unittest
from pathlib import Path


ROOT = Path(".forge/skills")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class DomainCorrectnessTest(unittest.TestCase):
    def test_security_has_no_unsupported_multiplier_or_httponly_immunity(self):
        security = read("ops/security/skill.tmpl.md")
        jwt = read("ops/security/references/jwt_hardening.md")
        self.assertNotIn("2.74x", security)
        self.assertNotIn("Immune to XSS", jwt)
        self.assertIn("does not make the app immune to XSS or CSRF", jwt)

    def test_gdpr_scope_uses_article_3_tests(self):
        gdpr = read("ops/legal/references/gdpr_dach_privacy.md")
        self.assertNotIn("If you have EU users, this applies to you.", gdpr)
        self.assertIn("EU establishment", gdpr)
        self.assertIn("offers goods or services", gdpr)
        self.assertIn("monitors their behavior", gdpr)

    def test_sales_forecast_does_not_invent_default_probabilities(self):
        pipeline = read("sales/pipeline/skill.tmpl.md")
        self.assertNotIn("Prospecting 10%", pipeline)
        self.assertIn("observed stage-to-close rates", pipeline)
        self.assertIn("unweighted forecast", pipeline)

    def test_venture_lists_all_nine_lean_canvas_blocks(self):
        venture = read("strategy/venture/skill.tmpl.md")
        self.assertIn("Unfair Advantage", venture)
        self.assertIn("all 9 boxes", venture)

    def test_accessibility_uses_wcag_not_lighthouse_as_conformance(self):
        a11y = read("engineering/frontend/references/accessibility_a11y.md")
        self.assertIn("WCAG 2.2 AA", a11y)
        self.assertIn("Lighthouse accessibility is a useful lab check", a11y)
        self.assertNotIn("Score MUST be 100", a11y)

    def test_store_policy_and_database_claims_are_currently_scoped(self):
        store = read("engineering/mobile/references/store_compliance.md")
        migration = read("engineering/database/references/migration_safety.md")
        self.assertIn("12 testers for at least 14 days", store)
        self.assertIn("Check the current guideline", store)
        self.assertNotIn("ALTER TABLE` on large tables without `CONCURRENTLY", migration)
        self.assertIn("Do not use invalid PostgreSQL", migration)

    def test_seo_does_not_optimize_for_leaked_fields(self):
        authority = read("marketing/seo/references/site_authority_signals.md")
        content = read("marketing/seo/references/content_eeat_protocol.md")
        self.assertIn("not as operating doctrine", authority)
        self.assertIn("not as operating doctrine", authority)
        self.assertIn("not optimize for leaked fields", authority)
        self.assertNotIn("bodyWordsToTokensRatio", content)

    def test_seo_uses_evidence_not_universal_content_quotas(self):
        files = [
            "marketing/seo/skill.tmpl.md",
            "marketing/seo/references/gsc_optimization_protocol.md",
            "marketing/seo/references/aeo_geo_protocol.md",
            "marketing/seo/references/quality_gates.md",
            "marketing/seo/references/content_eeat_protocol.md",
            "marketing/seo/references/technical_seo_protocol.md",
            "marketing/seo/references/topic_clustering_protocol.md",
            "marketing/seo/references/seo_audit_checklist.md",
        ]
        doctrine = "\n".join(read(path) for path in files)
        unsupported_quotas = [
            r"CTR\s*<\s*2%",
            r"134[-\u2013]167",
            r"40[-\u2013]60\s+words",
            r"1\s+(?:internal\s+|external\s+)?link\s+per\s+\d+",
            r"3[-\u2013]5\s+(?:new\s+)?(?:internal\s+)?links",
            r"Pillar\s+2,500[-\u2013]4,000",
        ]
        for pattern in unsupported_quotas:
            self.assertIsNone(re.search(pattern, doctrine, re.IGNORECASE), pattern)

        self.assertIn("Compare impressions, clicks, position, page job", doctrine)
        self.assertIn("A downward trend is an observation, not a diagnosis", doctrine)
        self.assertIn("primary or best available sources", doctrine)
        self.assertIn("schema_types_current.md", doctrine)
        self.assertIn("visible content and page type meet current eligibility", doctrine)


if __name__ == "__main__":
    unittest.main()

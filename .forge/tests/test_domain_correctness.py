"""Regression tests for high-risk domain doctrine."""
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


if __name__ == "__main__":
    unittest.main()

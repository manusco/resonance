import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FORGE = ROOT / ".forge"
if str(FORGE) not in sys.path:
    sys.path.insert(0, str(FORGE))

from schema_check import SchemaFailure, load_schema, validate
from test_eval_schemas import samples


class RuntimeSchemaCheckTests(unittest.TestCase):
    def test_all_public_contract_samples_pass_runtime_validation(self):
        for name, instance in samples().items():
            with self.subTest(name=name):
                validate(instance, load_schema(name))

    def test_missing_required_field_fails(self):
        instance = copy.deepcopy(samples()["evidence-manifest.schema.json"])
        del instance["runner"]
        with self.assertRaisesRegex(SchemaFailure, "missing runner"):
            validate(instance, load_schema("evidence-manifest.schema.json"))

    def test_unknown_schema_keyword_fails_closed(self):
        with self.assertRaisesRegex(SchemaFailure, "unsupported schema keywords"):
            validate("value", {"type": "string", "unimplementedKeyword": True})

    def test_unknown_keyword_in_unvisited_branches_fails_closed(self):
        schemas = [
            {"type": "object", "properties": {"absent": {"unknown": True}}},
            {"if": {"unknown": True}, "then": {"const": "x"}},
            {"not": {"unknown": True}},
        ]
        for schema in schemas:
            with self.subTest(schema=schema):
                with self.assertRaisesRegex(SchemaFailure, "unsupported schema keywords"):
                    validate({}, schema)


if __name__ == "__main__":
    unittest.main()
